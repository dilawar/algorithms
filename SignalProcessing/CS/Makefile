IMAGES= ./figure_compressend_sensing.pdf ./figure_solution.pdf \
	./figure_compressend_sensing_DCT.pdf ./figure_measurements.pdf

all : ./compressed_sensing.png ./magic_reconstruction.png  labnote.pdf labnote.html 
	@echo "All done"

labnote.pdf : labnote.pandoc $(IMAGES)
	~/Scripts/pandoc2pdf.sh $<

labnote.html : labnote.pandoc $(IMAGES)
	~/Scripts/pandoc2html.py $<

%.png : %.py 
	PYTHONPATH=~/Work/GITHUB/DILAWAR/pypgfplots/ python $<

%.pdf : %.tex
	lualatex --shell-escape $<
