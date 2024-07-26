#include <string>
#include <iostream>
using namespace std;

class Docente {
private:
    string nombre;
    string cedula;

public:
    void ingresarDatos();
    string getNombre();
    string getCedula();
};
void Docente::ingresarDatos() {
    cout << "Ingrese su nombre: ";
    cin >> nombre;
    do {
        cout << "Ingrese su cedula: ";
        cin >> cedula;
    } while(!validarCedula(cedula));
}

string Docente::getNombre() {
    return nombre;
}

string Docente::getCedula() {
    return cedula;
}

bool validarCedula(string cedula) {

    return true;
}
