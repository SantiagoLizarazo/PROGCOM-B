import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ejercicio1();
        ejercicio2();
        ejercicio3();
        ejercicio4();
        ejercicio5();
        ejercicio6();
        ejercicio7();
        ejercicio8();
        ejercicio9();
        ejercicio10();
    }

    // #1. Lista con los cuadrados del 1 al 10
    public static void ejercicio1() {
        ArrayList<Integer> cuadrados = new ArrayList<>();
        for (int i = 1; i <= 10; i++) {
            cuadrados.add(i * i);
        }
        System.out.println("Ejercicio 1: " + cuadrados);
    }

    // #2. Números pares del 0 al 20
    public static void ejercicio2() {
        ArrayList<Integer> numerosPares = new ArrayList<>();
        for (int i = 0; i <= 20; i++) {
            if (i % 2 == 0) {
                numerosPares.add(i);
            }
        }
        System.out.println("Ejercicio 2: " + numerosPares);
    }

    // #3. Doble de los números del 1 al 5
    public static void ejercicio3() {
        ArrayList<Integer> numerosDobles = new ArrayList<>();
        for (int i = 1; i <= 5; i++) {
            numerosDobles.add(i * 2);
        }
        System.out.println("Ejercicio 3: " + numerosDobles);
    }

    // #4. Extraer vocales de "programacion"
    public static void ejercicio4() {
        String palabra = "programacion";
        ArrayList<Character> vocales = new ArrayList<>();
        for (char letra : palabra.toCharArray()) {
            if ("aeiou".indexOf(letra) != -1) {
                vocales.add(letra);
            }
        }
        System.out.println("Ejercicio 4: " + vocales);
    }

    // #5. Palabras en mayúsculas
    public static void ejercicio5() {
        ArrayList<String> programas = new ArrayList<>();
        programas.add("python");
        programas.add("java");
        programas.add("c++");

        ArrayList<String> mayusculas = new ArrayList<>();
        for (String p : programas) {
            mayusculas.add(p.toUpperCase());
        }
        System.out.println("Ejercicio 5: " + mayusculas);
    }

    // #6. Clasificación par/impar
    public static void ejercicio6() {
        ArrayList<String> clasificacion = new ArrayList<>();
        for (int i = 1; i <= 10; i++) {
            if (i % 2 == 0) {
                clasificacion.add("par " + i);
            } else {
                clasificacion.add("impar " + i);
            }
        }
        System.out.println("Ejercicio 6: " + clasificacion);
    }

    // #7. Tuplas con número y cuadrado
    public static void ejercicio7() {
        ArrayList<String> numerosCuadrados = new ArrayList<>();
        for (int i = 1; i <= 5; i++) {
            numerosCuadrados.add(i + " su cuadrado es " + (i * i));
        }
        System.out.println("Ejercicio 7: " + numerosCuadrados);
    }

    // #8. Combinaciones de letras y números
    public static void ejercicio8() {
        String[] letras = {"a", "b"};
        int[] numeros = {1, 2, 3};

        ArrayList<String> combinados = new ArrayList<>();
        for (String letra : letras) {
            for (int numero : numeros) {
                combinados.add("(" + letra + "," + numero + ")");
            }
        }
        System.out.println("Ejercicio 8: " + combinados);
    }

    // #9. Palabras con más de 4 letras
    public static void ejercicio9() {
        ArrayList<String> palabras = new ArrayList<>();
        palabras.add("sol");
        palabras.add("estrella");
        palabras.add("mar");
        palabras.add("planeta");

        ArrayList<String> filtro = new ArrayList<>();
        for (String p : palabras) {
            if (p.length() > 4) {
                filtro.add(p);
            }
        }
        System.out.println("Ejercicio 9: " + filtro);
    }

    // #10. Clasificación de temperaturas
    public static void ejercicio10() {
        ArrayList<String> datos = new ArrayList<>();
        for (int x = 1; x <= 30; x++) {
            if (x < 26) {
                datos.add("frio " + x);
            } else if (x <= 29) {
                datos.add("templado " + x);
            } else {
                datos.add("caliente " + x);
            }
        }
        System.out.println("Ejercicio 10: " + datos);
    }
}