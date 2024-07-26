#include <iostream>
#include "Docente.h"
#include "Estudiante.h"
#include "Funciones.h"

using namespace std;

int main() {
    int opcion;
    do {
        cout << "Menu de Opciones" << endl;
        cout << "1. Ingresar datos del docente" << endl;
        cout << "2. Registrar notas" << endl;
        cout << "3. Ordenar calificaciones" << endl;
        cout << "4. Buscar calificación" << endl;
        cout << "5. Salir" << endl;
        cout << "Seleccione una opcion: ";
        cin >> opcion;

        switch(opcion) {
            case 1:
                ingresarDatosDocente();
                break;
            case 2:
                registrarNotas();
                break;
            case 3:
                ordenarCalificaciones();
                break;
            case 4:
                buscarCalificacion();
                break;
            case 5:
                cout << "Saliendo..." << endl;
                break;
            default:
                cout << "Opcion no valida" << endl;
        }
    } while(opcion != 5);
    return 0;
}
