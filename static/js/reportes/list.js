var urlapi = "https://cristhianog25.pythonanywhere.com/api/";
//http://127.0.0.1:8000/api/
//https://cristhianog25.pythonanywhere.com/api/
var map;
var markers = [];
var markerIdCounter = 0;
var startMarker = null;

var directionsService;
var directionsRenderer;
var tblReporte
$(function () {
     tblReporte = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: urlapi + 'get/reporte/',
            type: 'GET',
            dataSrc: "data"
        },
        columns: [
            {"data": "id"},
            {"data": "cliente.nombre"},
            {"data": "cliente.apellidos"},
            {"data": "descripcion"},
            {"data": "direccion"},
            {"data": "distrito.nombre_distrito"},
            {"data": "lat"},
            {"data": "long"},
            {"data": "created_at"},
            {"data": "id"}
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                render: function(data, type, row) {
                    if (type === 'display' || type === 'filter') {
                        var date = new Date(data);
                        return date.toLocaleDateString('es-ES', { 
                            day: '2-digit', 
                            month: '2-digit', 
                            year: 'numeric' 
                        });
                    }
                    return data;
                }
            },
            {
                targets: [-3, -4],
                class: 'text-center',
                render: function (data, type, row) {
                    return parseFloat(data).toFixed(6);
                }
            },
           
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" class="btn btn-success btn-xs" onclick="marcarCoordenadas(' + row.lat + ', ' + row.long + ',' + data + ')"><i class="fas fa-map-marker-alt"></i></a> ';
                    buttons += '<a href="#" class="btn btn-warning btn-xs" onclick="deleteMarcador(' + data + ')"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            llenarOpcionesDistrito(json.data);
        }
        });
        $('#btnFiltrar').on('click', function() {
            aplicarFiltros();
        });

        $('#btnLimpiarFiltros').on('click', function() {
            limpiarFiltros();
        });
});

function llenarOpcionesDistrito(data) {
    var distritos = [...new Set(data.map(item => item.distrito.nombre_distrito))];
    var selectDistrito = $('#filtroDistrito');
    distritos.forEach(distrito => {
        selectDistrito.append($('<option>', {
            value: distrito,
            text: distrito
        }));
    });
}

function aplicarFiltros() {
    var distritoSeleccionado = $('#filtroDistrito').val();
    var fechaSeleccionada = $('#filtroFecha').val();

    // Limpiar filtros anteriores
    tblReporte.search('').columns().search('').draw();

    // Aplicar filtro de distrito
    if (distritoSeleccionado) {
        tblReporte.column(5).search(distritoSeleccionado, true, false);
    }

    // Aplicar filtro de fecha
    if (fechaSeleccionada) {
        $.fn.dataTable.ext.search.push(
            function(settings, data, dataIndex) {
                var fechaCreacion = data[8]; // La fecha está en la columna 8 de la tabla
                if (!fechaCreacion) return false;
                
                // Convertir la fecha de creación al formato YYYY-MM-DD
                var partesFecha = fechaCreacion.split(/[/ :]/);
                if (partesFecha.length < 3) return false;
                
                var fechaFormateada = partesFecha[2] + '-' + 
                                      partesFecha[1].padStart(2, '0') + '-' + 
                                      partesFecha[0].padStart(2, '0');
                
                return fechaFormateada === fechaSeleccionada;
            }
        );
    }

    // Aplicar los filtros
    tblReporte.draw();

    // Limpiar el filtro de fecha personalizado
    if (fechaSeleccionada) {
        $.fn.dataTable.ext.search.pop();
    }
}
function limpiarFiltros() {
    // Limpiar los valores de los filtros
    $('#filtroDistrito').val('');
    $('#filtroFecha').val('');

    // Limpiar los filtros de la tabla
    tblReporte.search('').columns().search('').draw();

    // Eliminar cualquier filtro personalizado
    $.fn.dataTable.ext.search.pop();

    // Recargar los datos originales
    tblReporte.ajax.reload();
}
function initMap() {
    var chiclayo = { lat: -6.7739024, lng: -79.8603794 };
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: chiclayo
    });
    
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true // Esto evita que se reemplacen tus marcadores existentes
    });
}

function marcarCoordenadas(lat, lng, id) {
    // Verificar si ya existe un marcador con este ID
    var marcadorExistente = markers.find(function(marker) {
        return marker.id === id;
    });

    if (marcadorExistente) {
        alert("El marcador #" + id + " ya se encuentra en el mapa.");
        return; // Salir de la función sin agregar un nuevo marcador
    }

    // Limpiar la ruta existente si la hay
    if (directionsRenderer) {
        directionsRenderer.setMap(null);
        directionsRenderer.setMap(map);
    }

    var location = { lat: parseFloat(lat), lng: parseFloat(lng) };
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        label: id.toString(), 
        title: 'Marcador ' + id,
        id: id
    });
    markers.push(marker);

    // Centrar el mapa en el nuevo marcador
    map.setCenter(location);
}


function deleteMarcador(id) {
    var index = markers.findIndex(function(marker) {
        return marker.id === id;
    });

    if (index !== -1) {
        markers[index].setMap(null); // Eliminar el marcador del mapa
        markers.splice(index, 1); // Eliminar el marcador del array
        console.log("Marcador #" + id + " eliminado.");
    } else {
        console.log("Marcador #" + id + " no encontrado.");
    }
}

// function actualizarMarcadores() {
//     markers.forEach(function(marker, index) {
//         marker.label = (index + 1).toString();
//         marker.title = 'Marcador ' + (index + 1);
//         marker.markerId = index + 1;
//     });
// }

function eliminarTodosLosMarcadores() {
    markers.forEach(function(marker) {
        marker.setMap(null);
    });
    markers = [];
    if (directionsRenderer) {
        directionsRenderer.setMap(null);
    }
}

function calcularRutaOptima() {
    console.log("Iniciando cálculo de ruta");
    console.log("Número de marcadores:", markers.length);
    
    if (markers.length < 2) {
        alert("Se necesitan al menos dos marcadores para calcular una ruta.");
        return;
    }

    var waypoints = markers.slice(1, -1).map(function(marker) {
        return {
            location: marker.getPosition(),
            stopover: true
        };
    });

    console.log("Waypoints:", waypoints);

    var request = {
        origin: markers[0].getPosition(),
        destination: markers[markers.length - 1].getPosition(),
        waypoints: waypoints,
        optimizeWaypoints: true,
        travelMode: google.maps.TravelMode.DRIVING
    };

    console.log("Request:", request);

    directionsService.route(request, function(result, status) {
        console.log("Resultado del servicio de direcciones:", status);
        if (status === google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(result);
            console.log("Ruta trazada con éxito");
            
            var route = result.routes[0];
            var totalDistance = 0;
            var totalDuration = 0;
            var markerOrder = [];

            // Agregar el ID del marcador de inicio
            markerOrder.push(markers[0].id.toString());

            // Obtener el orden optimizado de los waypoints
            var waypointOrder = route.waypoint_order;
            
            for (var i = 0; i < route.legs.length; i++) {
                totalDistance += route.legs[i].distance.value;
                totalDuration += route.legs[i].duration.value;
                
                if (i < route.legs.length - 1) {
                    // Agregar los IDs de los marcadores intermedios en el orden optimizado
                    markerOrder.push(markers[waypointOrder[i] + 1].id.toString());
                }
            }

            // Agregar el ID del marcador final
            markerOrder.push(markers[markers.length - 1].id.toString());

            // Convertir distancia a kilómetros y duración a horas y minutos
            var distanceKm = (totalDistance / 1000).toFixed(2);
            var durationHours = Math.floor(totalDuration / 3600);
            var durationMinutes = Math.floor((totalDuration % 3600) / 60);

            // Actualizar la información en el HTML
            document.getElementById('tiempoRecorrido').textContent = durationHours + ' horas ' + durationMinutes + ' minutos';
            document.getElementById('distanciaTotal').textContent = distanceKm + ' km';
            document.getElementById('cantidadMarcadores').textContent = markers.length;
            document.getElementById('ordenMarcadores').textContent = markerOrder.join(' → ');

            // Ajustar el zoom y el centro del mapa para mostrar toda la ruta
            var bounds = new google.maps.LatLngBounds();
            route.overview_path.forEach(function(point) {
                bounds.extend(point);
            });
            map.fitBounds(bounds);
        } else {
            alert("No se pudo calcular la ruta: " + status);
        }
    });
}