// native/native.cpp
// Exemple de DLL native minimale exportant une fonction add

extern "C" __declspec(dllexport) int add(int a, int b) {
	return a + b;
}
