# g++ -o ProcessData_2023Mar1 ProcessData_2023Mar1.cpp -I/opt/homebrew/Cellar/range-v3/0.12.0/include `root-config --cflags --glibs` $(pkg-config --libs --cflags fmt)
# TARGET = ProcessData_2023Mar1
# TARGET = calculateHourglassUnc
TARGET = add_hourglass_unc
TARGET2 = add_hourglass_unc_VR
TARGET3 = add_hourglass_unc_VR_forLimits
CC = gcc
ROOTFLAGS  = `root-config --cflags --glibs`
CXXFLAGS += -Wall -Wformat
LDFLAGS="-Wl,--copy-dt-needed-entries"

$(TARGET): ../scripts/$(TARGET).C
	$(CC) $(CXXFLAGS) $(LDFLAGS) -o bin/$(TARGET) ../scripts/$(TARGET).C  $(ROOTFLAGS)

$(TARGET2): ../scripts/$(TARGET2).C
	$(CC) $(CXXFLAGS) $(LDFLAGS) -o bin/$(TARGET2) ../scripts/$(TARGET2).C  $(ROOTFLAGS)

$(TARGET3): ../scripts/$(TARGET3).C
	$(CC) $(CXXFLAGS) $(LDFLAGS) -o bin/$(TARGET3) ../scripts/$(TARGET3).C  $(ROOTFLAGS)

clean:
	@rm hourglassUnc/bin/$(TARGET) hourglassUnc/bin/$(TARGET2) hourglassUnc/bin/$(TARGET3)
