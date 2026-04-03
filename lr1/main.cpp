#include <iostream>
#include <fstream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    std::string filename = "document.docx";
    
    try {
        if (!fs::exists(filename)) {
            std::cerr << "Ошибка: файл '" << filename << "' не найден!" << std::endl;
            return 1;
        }
        std::uintmax_t fileSize = fs::file_size(filename);
        std::cout << "Размер файла '" << filename << "': " << fileSize << " байт" << std::endl;
    } catch (const fs::filesystem_error& e) {
        std::cerr << "Ошибка файловой системы: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
