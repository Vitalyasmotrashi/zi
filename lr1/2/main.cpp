#include <iostream>
#include <fstream>
#include <iomanip>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Использование: " << argv[0] << " <имя_файла>" << std::endl;
        return 1;
    }
    
    std::string filename = argv[1];
    
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << filename << "'" << std::endl;
        return 1;
    }
    
    unsigned long long frequency[256] = {0};
    unsigned long long totalBytes = 0;
    
    char byte;
    while (file.get(byte)) {
        frequency[static_cast<unsigned char>(byte)]++;
        totalBytes++;
    }
    
    file.close();
    
    std::cout << "файл: " << filename << std::endl;
    std::cout << "байт: " << totalBytes << std::endl;
    std::cout << "\n--- Частоты ---\n" << std::endl;
    
    std::cout << std::setw(6) << "Байт" 
              << std::setw(8) << "HEX" 
              << std::setw(10) << "DEC"
              << std::setw(15) << "Количество" 
              << std::setw(12) << "Частота (%)" << std::endl;
    std::cout << std::string(51, '-') << std::endl;
    
    for (int i = 0; i < 256; i++) {
        if (frequency[i] > 0) {
            double percentage = (static_cast<double>(frequency[i]) / totalBytes) * 100.0;
            
            std::cout << std::setw(6);
            if (i >= 32 && i < 127) {
                std::cout << "'" << static_cast<char>(i) << "'";
            } else {
                std::cout << "---";
            }
            
            std::cout << std::setw(8) << std::hex << std::uppercase << i << std::dec
                      << std::setw(10) << i
                      << std::setw(15) << frequency[i]
                      << std::setw(11) << std::fixed << std::setprecision(4) << percentage << "%"
                      << std::endl;
        }
    }
    
    return 0;
}
