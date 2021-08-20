CC       = g++
CPPFLAGS = -std=c++17 -g -I `root-config --incdir` -O3
OBJFLAGS  = $(CPPFLAGS) -fPIC
LDFLAGS = $(CPPFLAGS)
LDLIBS  = -lRooFit -lRooFitCore `root-config --libs`

TestInterpolatorHist2D2D: TestInterpolatorHist2D2D.o RooMomentMorphND_local.o
	$(CC) $(LDFLAGS) TestInterpolatorHist2D2D.o RooMomentMorphND_local.o -o TestInterpolatorHist2D2D $(LDLIBS)

TestInterpolatorHist2D2D.o: TestInterpolatorHist2D2D.cc RooMomentMorphND_local.h
	$(CC) $(OBJFLAGS) -c TestInterpolatorHist2D2D.cc

RooMomentMorphND_local.o: RooMomentMorphND_local.cpp
	$(CC) $(OBJFLAGS) -c RooMomentMorphND_local.cpp

clean:
	rm *.o TestInterpolatorHist2D2D



# g++ -std=c++17 -g -o3 -fPIC -I `root-config --incdir` -c RooMomentMorphND_local.cpp -o RooMomentMorphND_local.o 
# g++  -std=c++17 -g -I `root-config --incdir` -lRooFit -lRooFitCore -o TestInterpolatorHist2D2D TestInterpolatorHist2D2D.cc `root-config --libs` -O3 RooMomentMorphND_local.o