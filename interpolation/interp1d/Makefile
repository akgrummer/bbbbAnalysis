# g++ -o ProcessData_2023Mar1 ProcessData_2023Mar1.cpp -I/opt/homebrew/Cellar/range-v3/0.12.0/include `root-config --cflags --glibs` $(pkg-config --libs --cflags fmt)
# TARGET = ProcessData_2023Mar1
TARGET = th1morph
CC = gcc
ROOTFLAGS  = `root-config --cflags --glibs`
CXXFLAGS += -Wall -Wformat
LDFLAGS="-Wl,--copy-dt-needed-entries"
RANGEFLAGS = -I/uscms/home/agrummer/nobackup/range-v3/include/
YAMLFLAGS = -I/uscms/home/agrummer/nobackup/yaml-cpp/include/ -L/uscms/home/agrummer/nobackup/yaml-cpp/build/ -lyaml-cpp

$(TARGET):
	$(CC) $(CXXFLAGS) $(LDFLAGS) -o bin/$(TARGET) $(TARGET).C  $(RANGEFLAGS) $(YAMLFLAGS) $(ROOTFLAGS)

clean:
	@rm $(TARGET)
