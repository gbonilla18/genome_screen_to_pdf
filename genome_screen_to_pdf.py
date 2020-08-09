#!/usr/bin/env python
# FILE: genome_screen_to_pdf.py
# PURPOSE: retrieve pdfs from the UCSC genome browser using query strings
# AUTHOR: G.Bonilla
# CREATE DATE: 4/24/2013
# UPDATE: 7/18/2016 can load the page with the link to the pdf automatically, without loading the location first

import glob
import re
import sys
import urllib.parse
import urllib.request
import optparse

import os
import time

import argparse


parser = argparse.ArgumentParser(description="Script to automate capture of UCSC screenshots. By G. Bonilla. https://github.com/gbonilla18/genome_screen_to_pdf")
parser.add_argument("-r","--regions",type=argparse.FileType('r'),required=True,help="File containing genomic regions to be captured, in BED format (four columns). Required.")
parser.add_argument("-s","--hgsid",type=str,required=True,help="ID of the UCSC genome browser session that will be used for the screenshots. Can be obtained from the URL: http://genome.ucsc.edu/cgi-bin/hgTracks?hgsid=<SESSION_ID>. Required.")
parser.add_argument("-g","--genome",type=str,required=True,help="Genome keyword used by the UCSC genome browser, e.g. mm9, hg19. Required")
parser.add_argument("-o","--out-prefix",type=str,default="screenshot_",help="Output file name prefix. Will be used to label the individual PDFs and the merged file.")
parser.add_argument("-m","--merge",action="store_true",help="If specified, the screenshots will be merged into one PDF file. This option requires Ghostscript.")
parser.add_argument("-d","--dist",type=int,default=10000,help="Distance in bp. that will be added to each side of the genomic feature. Default: 10000 bp.")

args = parser.parse_args()


def get_page(query_str):
        #print("retrieving page ...")
        #print(query_str)
        with urllib.request.urlopen(query_str) as response:
                u_page = response.read()
        text_page=u_page.decode('utf-8')
        #print(len(text_page))
        return text_page

def get_pdf(chr,start,end,site_id,genome_db,hgsid,bname):

        base_link="https://genome.ucsc.edu/"

        chr_loc="%s:%s-%s"%(chr,start,end)
        safe_chr_loc=urllib.parse.quote_plus(chr_loc)
        #print(safe_chr_loc)

        #old query
        ucsc_query_str="cgi-bin/hgTracks?db=%s&position=%s&hgsid=%s"%(genome_db,safe_chr_loc,hgsid)

        #new query, with psOutput-on already
        ucsc_query_str="cgi-bin/hgTracks?db=%s&position=%s&hgsid=%s&hgt.psOutput=on"%(genome_db,safe_chr_loc,hgsid)

        safe_str=ucsc_query_str
        #print(safe_str)
        ucsc_page = get_page(base_link+safe_str)
        #print(ucsc_page)


        # pn=re.compile("\./(.*psOutput.*)'\sid")
        # view_link=pn.findall(ucsc_page)
        # aug_link=base_link+view_link[0]
        # print aug_link
        # view_page=get_page(aug_link)

        ppdf=re.compile("\.\.(.*hgt_genome.*pdf)")
        # pdf_link=ppdf.findall(view_page) # old version
        pdf_link=ppdf.findall(ucsc_page) # new version


        aug_pdf_link=base_link+pdf_link[0]

        pdf_file_name=bname+'_'+re.sub(':','_',chr_loc)+'_ID_'+site_id+'.pdf'

        shell_cmd="curl -o %s %s"%(pdf_file_name,aug_pdf_link)

        #print(shell_cmd)

        os.system(shell_cmd)

        #time.sleep(10)
        return pdf_file_name

print(args)

genome_db=args.genome
hgsid=args.hgsid
chr_locations_f=args.regions
output_bname=args.out_prefix
dist=args.dist
merge_flag=args.merge

# chr_locations_f=open(bed_file)
chr_locations=chr_locations_f.readlines()
chr_locations_f.close()

pdf_fnames=[]
for chr_loc in chr_locations:
        chr_loc_spl=chr_loc.strip().split("\t")
        chr=chr_loc_spl[0]
        start=chr_loc_spl[1]
        end=chr_loc_spl[2]
        site_id=chr_loc_spl[3]

        new_start=int(start)-dist
        new_end=int(end)+dist

        pdf_fnames.append(get_pdf(chr,new_start,new_end,site_id,genome_db,hgsid,output_bname))

all_pdf_names=" ".join(pdf_fnames)
print(all_pdf_names)

#merge all files into one pdf
if(merge_flag):
    shell_merge_cmd="gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=%s_merged.pdf %s"%(output_bname,all_pdf_names)
    #print(shell_merge_cmd)
    os.system(shell_merge_cmd)
