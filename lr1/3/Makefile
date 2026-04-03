CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
TARGET = cipher
SRC = main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET) encrypted.txt decrypted.txt

.PHONY: all clean
