CC       = g++
CPPFLAGS = -std=c++17 -g -I `root-config --incdir` -O3
OBJFLAGS  = $(CPPFLAGS) -fPIC
LDFLAGS = $(CPPFLAGS)
LDLIBS  = -lRooFit -lRooFitCore `root-config --libs`

# example:
	# $(CC) $(LDFLAGS) example.cc -o example $(LDLIBS)

InterpolateSignals: InterpolateSignals.o
	$(CC) $(LDFLAGS) InterpolateSignals.o -o InterpolateSignals $(LDLIBS)

InterpolateSignals.o: InterpolateSignals.cc
	$(CC) $(OBJFLAGS) -c InterpolateSignals.cc
#
# TestInterpolatorHist2D2D: TestInterpolatorHist2D2D_2023Apr26.o
# 	$(CC) $(LDFLAGS) TestInterpolatorHist2D2D_2023Apr26.o -o TestInterpolatorHist2D2D $(LDLIBS)
#
# TestInterpolatorHist2D2D_2023Apr26.o: TestInterpolatorHist2D2D_2023Apr26.cc
# 	$(CC) $(OBJFLAGS) -c TestInterpolatorHist2D2D_2023Apr26.cc

clean:
	rm *.o InterpolateSignals



# g++ -std=c++17 -g -o3 -fPIC -I `root-config --incdir` -c RooMomentMorphND_local.cpp -o RooMomentMorphND_local.o
# g++  -std=c++17 -g -I `root-config --incdir` -lRooFit -lRooFitCore -o TestInterpolatorHist2D2D TestInterpolatorHist2D2D.cc `root-config --libs` -O3 RooMomentMorphND_local.o
