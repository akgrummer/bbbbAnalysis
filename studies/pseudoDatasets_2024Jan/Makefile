# g++ -o ProcessData_2023Mar1 ProcessData_2023Mar1.cpp -I/opt/homebrew/Cellar/range-v3/0.12.0/include `root-config --cflags --glibs` $(pkg-config --libs --cflags fmt)
# TARGET = ProcessData_2023Mar1
# TARGET = calculateHourglassUnc
TARGET = createPsuedoDataset_localExcess_2024Jan
CC = gcc
ROOTFLAGS  = `root-config --cflags --glibs`
CXXFLAGS += -Wall -Wformat
LDFLAGS="-Wl,--copy-dt-needed-entries"

$(TARGET): ../../scripts/$(TARGET).cpp
	$(CC) $(CXXFLAGS) $(LDFLAGS) -o bin/$(TARGET) ../../scripts/$(TARGET).cpp  $(ROOTFLAGS)

clean:
	@rm studies/pseudoDatasets_2024Jan/bin/$(TARGET)

