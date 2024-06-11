CC       = g++
CPPFLAGS = -std=c++17 -g -I `root-config --incdir` -O3
OBJFLAGS  = $(CPPFLAGS) -fPIC
LDFLAGS = $(CPPFLAGS)
LDLIBS  = -lRooFit -lRooFitCore `root-config --libs`

# example:
	# $(CC) $(LDFLAGS) example.cc -o example $(LDLIBS)

fill_histograms: obj/fill_histograms.o
	$(CC) $(LDFLAGS) obj/fill_histograms.o -o bin/fill_histograms $(LDLIBS)

obj/fill_histograms.o: fill_histograms.cpp
	$(CC) $(OBJFLAGS) -c $< -o $@
#
# TestInterpolatorHist2D2D: TestInterpolatorHist2D2D_2023Apr26.o
# 	$(CC) $(LDFLAGS) TestInterpolatorHist2D2D_2023Apr26.o -o TestInterpolatorHist2D2D $(LDLIBS)
#
# TestInterpolatorHist2D2D_2023Apr26.o: TestInterpolatorHist2D2D_2023Apr26.cc
# 	$(CC) $(OBJFLAGS) -c TestInterpolatorHist2D2D_2023Apr26.cc

# https://stackoverflow.com/a/3148530
clean:
	-@rm obj/*.o bin/fill_histograms 2>/dev/null || true



# g++ -std=c++17 -g -o3 -fPIC -I `root-config --incdir` -c RooMomentMorphND_local.cpp -o RooMomentMorphND_local.o
# g++  -std=c++17 -g -I `root-config --incdir` -lRooFit -lRooFitCore -o TestInterpolatorHist2D2D TestInterpolatorHist2D2D.cc `root-config --libs` -O3 RooMomentMorphND_local.o
