# genome_screen_to_pdf.py

## Description

genome_screen_to_pdf.py is a command-line utility written in python 3 to enable the automated capture of screenshots from the [UCSC genome browser](https://genome.ucsc.edu). This utility allows the capture of screenshots for multiple regions specified in a [BED file](https://genome.ucsc.edu/FAQ/FAQformat.html#format1), and provides the output as PDF files, with the option of concatenating all screenshots into one PDF file.

| Parameter                              | Description                                                                                                                                                                      |
|----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -r REGIONS, --regions REGIONS          | File containing genomic regions to be captured, in BED format (four columns). Required.                                                                                          |
| -s HGSID, --hgsid HGSID                | ID of the UCSC genome browser session that will be used for the screenshots. Can be obtained from the URL: http://genome.ucsc.edu/cgi-bin/hgTracks?hgsid=<SESSION_ID>. Required. |
| -g GENOME, --genome GENOME             | Genome keyword used by the UCSC genome browser, e.g. mm9, hg19. Required                                                                                                         |
| -o OUT_PREFIX, --out-prefix OUT_PREFIX | Output file name prefix. Will be used to label the individual PDFs and the merged file.                                                                                          |
| -m, --merge                            | If specified, the screenshots will be merged into one PDF file. This option requires Ghostscript.                                                                                |
| -d DIST, --dist DIST                   | Distance in bp. that will be added to each side of the genomic feature. Default: 10000 bp.                                                                                       |


## Dependencies

Optional:
[Ghostscript](http://www.ghostscript.com/) is used to merge PDFs into one file.

## Usage

Example:

```bash
python genome_screen_to_pdf.py -r lncRNAs_27h_DHS.bed -s 370994213_UE99C07Nj9OAzhhKlDUQjc9Hs88q -g mm9 -o lncRNA_screenshots -d 10000
```

