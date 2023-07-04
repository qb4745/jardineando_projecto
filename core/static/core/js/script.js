$(document).ready(function () {
    // Realizar la solicitud a la API
    $.getJSON("https://sinca.mma.gob.cl/index.php/json/listadomapa2k19/", function (data) {
        var selectElemento = $("#select-elemento");
        var tablaDatos = $("#tabla-datos");

        // Ordenar el arreglo de elementos alfabéticamente
        data.sort(function (a, b) {
            return a.nombre.localeCompare(b.nombre);
        });
        // Agregar la opción por defecto al combobox
        selectElemento.append('<option value="">Seleccione una ciudad...</option>');

        // Llenar el combobox de elementos ordenados
        $.each(data, function (index, elemento) {
            $("<option>").text(elemento.nombre).appendTo(selectElemento);
        });

        // Función para filtrar los datos y actualizar la tabla
        function filtrarDatos(elementoSeleccionado) {
            tablaDatos.empty();

            // Buscar el elemento seleccionado en los datos
            var elemento = data.find(function (item) {
                return item.nombre === elementoSeleccionado;
            });

            // Verificar si se encontró el elemento
            if (elemento) {
                // Crear la tabla y encabezados
                var table = $("<table>").addClass("data-table").css("border-collapse", "separate");
                var thead = $("<thead>").appendTo(table);
                var tbody = $("<tbody>").appendTo(table);
                var headerRow = $("<tr>").appendTo(thead);
                $("<th>").text("Fecha").appendTo(headerRow);
                $("<th>").text("Valor").appendTo(headerRow);
                $("<th>").text("Nivel").appendTo(headerRow);

                // Recorrer los datos en tiempo real y agregar filas a la tabla
                $.each(elemento.realtime, function (index, item) {
                    var rowData = item.info.rows[0].c;
                    var fecha = rowData[0].v;
                    var valor = rowData[1].v;
                    var nivel = obtenerNivel(valor);

                    var dataRow = $("<tr>").appendTo(tbody);
                    $("<td>").text(fecha).appendTo(dataRow);
                    $("<td>").text(valor).css({
                        "font-weight": "bold",
                        "padding": "8px"
                    }).appendTo(dataRow);
                    $("<td>").text(nivel).addClass(obtenerClaseNivel(nivel)).css({
                        "font-weight": "bold",
                        "color": obtenerColorNivel(nivel),
                        "padding": "8px",
                        "border": "1px solid " + obtenerColorNivel(nivel)
                    }).appendTo(dataRow);
                });

                // Agregar la tabla a la página
                tablaDatos.append(table);
            } else {
                // Mostrar un mensaje si no se encontró el elemento
                tablaDatos.text("Elemento no encontrado");
            }
        }

        // Obtener el nivel correspondiente según el valor
        function obtenerNivel(valor) {
            if (valor <= 50) {
                return "Bueno";
            } else if (valor <= 100) {
                return "Moderado";
            } else {
                return "Malo";
            }
        }

        // Obtener la clase CSS correspondiente al nivel
        function obtenerClaseNivel(nivel) {
            if (nivel === "Bueno") {
                return "bueno";
            } else if (nivel === "Moderado") {
                return "moderado";
            } else {
                return "malo";
            }
        }

        // Obtener el color correspondiente al nivel
        function obtenerColorNivel(nivel) {
            if (nivel === "Bueno") {
                return "green";
            } else if (nivel === "Moderado") {
                return "orange";
            } else {
                return "red";
            }
        }

        // Manejar el evento de cambio en el combobox de elementos
        selectElemento.on("change", function () {
            var elementoSeleccionado = $(this).val();
            filtrarDatos(elementoSeleccionado);
        });
    });
});
