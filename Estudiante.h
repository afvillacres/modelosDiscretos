#include <string>
#include <iostream>

using namespace std;

class Estudiante {
private:
    string apellido;
    string correo;
    float notas[3]; // Suponiendo que hay 3 notas por estudiante

public:
    void ingresarDatos();
    float calcularPromedio();
};

void Estudiante::ingresarDatos() {
    cout << "Ingrese apellido: ";
    cin >> apellido;
    cout << "Ingrese correo: ";
    cin >> correo;
    for(int i = 0; i < 3; i++) {
        do {
            cout << "Ingrese nota " << i+1 << " (0-20): ";
            cin >> notas[i];
        } while(notas[i] < 0 || notas[i] > 20);
    }
}

float Estudiante::calcularPromedio() {
    float suma = 0;
    for(int i = 0; i < 3; i++) {
        suma += notas[i];
    }
    return suma / 3;
}
