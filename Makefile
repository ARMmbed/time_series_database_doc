all: aws_flow.png

%.png: %.svg
	inkscape --export-png=$@ $<
