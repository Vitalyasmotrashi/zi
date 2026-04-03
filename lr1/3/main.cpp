#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

const int COLUMNS = 5;

// ключ
std::vector<int> readKey(const std::string& keyFile) {
    std::ifstream file(keyFile);
    if (!file) {
        std::cerr << keyFile << "'" << std::endl;
        exit(1);
    }
    
    std::vector<int> key(COLUMNS);
    for (int i = 0; i < COLUMNS; i++) {
        if (!(file >> key[i])) {
            std::cerr << COLUMNS << " чисел." << std::endl;
            exit(1);
        }
    }
    
    // должна быть перестановка 0..4
    std::vector<int> sorted_key = key;
    std::sort(sorted_key.begin(), sorted_key.end());
    for (int i = 0; i < COLUMNS; i++) {
        if (sorted_key[i] != i) {
            std::cerr << "Err: ключ должен быть перестановкой чисел 0-" << (COLUMNS - 1) << std::endl;
            exit(1);
        }
    }
    
    file.close();
    return key;
}

std::vector<char> readFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "Err: '" << filename << "'" << std::endl;
        exit(1);
    }
    
    std::vector<char> data((std::istreambuf_iterator<char>(file)),
                           std::istreambuf_iterator<char>());
    file.close();
    return data;
}

// запись 
void writeFile(const std::string& filename, const std::vector<char>& data) {
    std::ofstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "Err: не удалось создать файл '" << filename << "'" << std::endl;
        exit(1);
    }
    
    file.write(data.data(), data.size());
    file.close();
}

// шифрование
std::vector<char> encrypt(const std::vector<char>& input, const std::vector<int>& key) {
    std::vector<char> data = input;
    
    // 'z' 
    while (data.size() % COLUMNS != 0) {
        data.push_back('z');
    }
    
    int rows = data.size() / COLUMNS;
    std::vector<char> result;
    result.reserve(data.size());
    
    // по столбцам в порядке, заданном ключом
    for (int k = 0; k < COLUMNS; k++) {
        int col = key[k];  
        for (int row = 0; row < rows; row++) {
            result.push_back(data[row * COLUMNS + col]);
        }
    }
    
    return result;
}

// расшифрование
std::vector<char> decrypt(const std::vector<char>& input, const std::vector<int>& key) {
    if (input.size() % COLUMNS != 0) {
        std::cerr << "Ошибка: размер зашифрованного файла должен быть кратен " << COLUMNS << std::endl;
        exit(1);
    }
    
    int rows = input.size() / COLUMNS;
    std::vector<char> result(input.size());
    
    // обратная операция: записываем по столбцам в порядке ключа
    int pos = 0;
    for (int k = 0; k < COLUMNS; k++) {
        int col = key[k];  // номер столбца для записи
        for (int row = 0; row < rows; row++) {
            result[row * COLUMNS + col] = input[pos++];
        }
    }
    
    // 'z' в конце
    while (!result.empty() && result.back() == 'z') {
        result.pop_back();
    }
    
    return result;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cout << "Использование:" << std::endl;
        std::cout << "  Шифрование:   " << argv[0] << " -e <входной_файл> <выходной_файл>" << std::endl;
        std::cout << "  Расшифрование: " << argv[0] << " -d <входной_файл> <выходной_файл>" << std::endl;
        std::cout << "\nКлюч читается из файла 'key.txt'" << std::endl;
        return 1;
    }
    
    std::string mode = argv[1];
    std::string inputFile = argv[2];
    std::string outputFile = argv[3];
    
    // ключ
    std::vector<int> key = readKey("key.txt");
    
    std::cout << "Ключ: ";
    for (int i = 0; i < COLUMNS; i++) {
        std::cout << key[i] << " ";
    }
    std::cout << std::endl;
    
    // входной файл
    std::vector<char> inputData = readFile(inputFile);
    std::cout << "Размер входного файла: " << inputData.size() << " байт" << std::endl;
    
    std::vector<char> outputData;
    
    if (mode == "-e") {
        // шифрование
        outputData = encrypt(inputData, key);
        std::cout << "Режим: шифрование" << std::endl;
        std::cout << "Размер выходного файла: " << outputData.size() << " байт" << std::endl;
    } else if (mode == "-d") {
        // расшифрование
        outputData = decrypt(inputData, key);
        std::cout << "Режим: расшифрование" << std::endl;
        std::cout << "Размер выходного файла: " << outputData.size() << " байт" << std::endl;
    } else {
        std::cerr << "Ошибка: неверный режим. Используйте -e для шифрования или -d для расшифрования" << std::endl;
        return 1;
    }
    
    writeFile(outputFile, outputData);
    std::cout << "результат сохранен в '" << outputFile << "'" << std::endl;
    
    return 0;
}
