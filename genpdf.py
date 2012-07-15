#!/usr/bin/python
# -*- coding: utf-8 -*-

import sx.pisa3 as pisa

def genpdf(html_name, pdf_name):
    data = open(html_name).read()
    f = file(pdf_name,'w')
    pdf = pisa.CreatePDF(data,f)
    f.close()
    return
    