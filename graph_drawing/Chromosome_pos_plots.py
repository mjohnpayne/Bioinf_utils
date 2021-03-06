__author__ = 'mjohnpayne'

from Bio import SeqIO
from reportlab.lib.units import cm
import reportlab.lib.colors as colours
from Bio.Graphics import BasicChromosome
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.Alphabet import IUPAC
import sys

ingff = open('/Users/mjohnpayne/Documents/PhD/wt_genome/pmfa1_working_models_fix.gff3','r')

print len(sys.argv)

def remove_dupes(ls):
    ls = list(set(ls))
    return ls


if len(sys.argv) == 3:
    acclis1 = remove_dupes(open(sys.argv[1],'r').read().split())
elif len(sys.argv) == 4:
    acclis1 = remove_dupes(open(sys.argv[1],'r').read().split())
    acclis2 = remove_dupes(open(sys.argv[2],'r').read().split())
elif len(sys.argv) == 5:
    acclis1 = remove_dupes(open(sys.argv[1],'r').read().split())
    acclis2 = remove_dupes(open(sys.argv[2],'r').read().split())
    acclis3 = remove_dupes(open(sys.argv[3],'r').read().split())

elif len(sys.argv) == 6:
    acclis1 = remove_dupes(open(sys.argv[1],'r').read().split())
    acclis2 = remove_dupes(open(sys.argv[2],'r').read().split())
    acclis3 = remove_dupes(open(sys.argv[3],'r').read().split())
    acclis4 = remove_dupes(open(sys.argv[4],'r').read().split())
out = sys.argv[-1]

centromeres = {"c-100":["100",2110000, 2140000,None,""],'c-102': ["102",2610000, 2640000,None,""], 'c-103': ["103",1520000, 1550000,None,""],'c-93': ["93",1350000, 1370000,None,""],'c-95': ["95",760000, 790000,None,""],'c-96': ["96",3520000, 3550000,None,""],'c-99': ['99',2850000, 2880000,None,""],'c-97': ['97',2050000, 2070000,None,""]}

cent_list = ["c-100","c-99","c-102","c-103","c-93","c-95","c-96","c-97"]


##Extract gene position, contig and orientation info from gff
contigs = {}
gene = {}
for line in ingff:
        col = line.strip('\n').split('\t')
        if 'ID=gene' in line:
            det = col[8].split(';')
            pmaa = det[1][5:]
            st = int(col[3])
            en = int(col[4])
            orient = col[6]
            cont = col[0]
            if pmaa not in gene:
                if cont in contigs:
                        contigs[cont] += [pmaa]
                elif cont not in contigs:
                        contigs[cont] = [pmaa]
                gene[pmaa] = [cont,st,en,orient]

for cont in contigs:
        contigs[cont] = sorted(contigs[cont])

## Generate list of contig,length tuples then sort in decending order
genome = {}
entries = []
lengths = []
for i in SeqIO.parse("/Users/mjohnpayne/Documents/PhD/wt_genome/pmfa1_annot_scaf.fasta", "fasta"):
    genome[i.id] = i
    entries.append((i.id,len(i.seq)))
    lengths.append(len(i.seq))

entries = sorted(entries,key=lambda x: x[1],reverse=True)
## Create gene SeqFeatures as subsets of contig seqRecord objects
for i in genome:
    for j in gene:
        if gene[j][0] == genome[i].id:
            direc = int(gene[j][3] + '1')
            genome[i].features.append(SeqFeature(FeatureLocation(gene[j][1], gene[j][2], strand = direc),type='gene',id=j,qualifiers={'locus_tag':[j]}))
    for j in centromeres:
        if centromeres[j][0] == genome[i].id:
            # print j,gene[j][0],gene[j][3],genome[i].id
            # sl(0.5)
            direc = None#int(gene[j][3] + '1')
            genome[i].features.append(SeqFeature(FeatureLocation(centromeres[j][1], centromeres[j][2], strand = direc),type='gene',id=j,qualifiers={'locus_tag':[centromeres[j][4]]}))


## telomere length - rounded ends of chromosome size
max_len = max(lengths)
telomere_length = 40000

chr_diagram = BasicChromosome.Organism()
#chr_diagram.page_size = (60*cm, 21*cm)
chr_diagram.page_size = (40*cm, 21*cm)

fill = colours.CMYKColorSep(0.4, 0, 0, 0.3,density=0.4, spotName='PMS_7496')

for index, (name, length) in enumerate(entries):
    if length > 80000:
        features = []
        for i in acclis1:
            for f in genome[name].features:
                if f.id==i:
                    f.qualifiers['color'] = [2]
                    features += [f]
        for i in cent_list:
            for f in genome[name].features:
                if f.id==i:
                    f.qualifiers['color'] = ["grey"]
                    features += [f]
        if len(sys.argv) == 4:
            for i in acclis2:
                for f in genome[name].features:
                    if f.id==i:
                        f.qualifiers['color'] = [4]
                        features += [f]
        elif len(sys.argv) == 5:
            for i in acclis2:
                for f in genome[name].features:
                    if f.id==i:
                        f.qualifiers['color'] = [4]
                        features += [f]
            for i in acclis3:
                for f in genome[name].features:
                    if f.id==i:
                        f.qualifiers['color'] = [8]
                        features += [f]
        elif len(sys.argv) == 6:
            for i in acclis2:
                for f in genome[name].features:
                    if f.id==i:
                        f.qualifiers['color'] = [4]
                        features += [f]
            for i in acclis3:
                for f in genome[name].features:
                    if f.id==i:
                        f.qualifiers['color'] = [8]
                        features += [f]
            for i in acclis4:
                for f in genome[name].features:
                    if f.id==i:
                        f.qualifiers['color'] = [10]
                        features += [f]
        #for f in features: f.qualifiers["color"] = [index+2]
        cur_chromosome = BasicChromosome.Chromosome(name)
        cur_chromosome.scale_num = max_len + 2 * telomere_length
        cur_chromosome.label_size = 8
        cur_chromosome.chr_percent = 0.2
        cur_chromosome.label_sep_percent = 0.1


        #Add an opening telomere
        start = BasicChromosome.TelomereSegment()
        start.fill_color = fill
        start.scale = telomere_length
        cur_chromosome.add(start)

        #Add a body - using bp as the scale length here.
        body = BasicChromosome.AnnotatedChromosomeSegment(length,features)
        body.scale = length
        body.fill_color = fill
        cur_chromosome.add(body)

        #Add a closing telomere
        end = BasicChromosome.TelomereSegment(inverted=True)
        end.fill_color = fill
        end.scale = telomere_length
        cur_chromosome.add(end)

        #This chromosome is done
        chr_diagram.add(cur_chromosome)

scale = BasicChromosome.Chromosome('Legend')
scale.scale_num = max_len + 2 * telomere_length
scale.label_size = 8
scale.chr_percent = 0.3
scale.label_sep_percent = 0.12


acc1id = sys.argv[1].split('/')[-1].replace('.txt','')
feats = [SeqFeature(FeatureLocation(100000, 100500, strand = 1),type='gene',id=acc1id,qualifiers={'locus_tag':[acc1id],'color':[2]})]

accid = "Putative Centromeres"
feats += [SeqFeature(FeatureLocation(900000, 900500, strand = 1),type='gene',id=accid,qualifiers={'locus_tag':[accid],'color':["grey"]})]

if len(sys.argv) == 4:
    acc2id = sys.argv[2].split('/')[-1].replace('.txt','')
    feats += [SeqFeature(FeatureLocation(300000, 300500, strand = 1),type='gene',id=acc2id,qualifiers={'locus_tag':[acc2id],'color':[4]})]

if len(sys.argv) == 5:
    acc2id = sys.argv[2].split('/')[-1].replace('.txt','')
    feats += [SeqFeature(FeatureLocation(300000, 300500, strand = 1),type='gene',id=acc2id,qualifiers={'locus_tag':[acc2id],'color':[4]})]
    acc3id = sys.argv[3].split('/')[-1].replace('.txt','')
    feats += [SeqFeature(FeatureLocation(500000, 500500, strand = 1),type='gene',id=acc2id,qualifiers={'locus_tag':[acc3id],'color':[8]})]

if len(sys.argv) == 6:
    acc2id = sys.argv[2].split('/')[-1].replace('.txt','')
    feats += [SeqFeature(FeatureLocation(300000, 300500, strand = 1),type='gene',id=acc2id,qualifiers={'locus_tag':[acc2id],'color':[4]})]
    acc3id = sys.argv[3].split('/')[-1].replace('.txt','')
    feats += [SeqFeature(FeatureLocation(500000, 500500, strand = 1),type='gene',id=acc2id,qualifiers={'locus_tag':[acc3id],'color':[8]})]
    acc4id = sys.argv[4].split('/')[-1].replace('.txt','')
    feats += [SeqFeature(FeatureLocation(700000, 700500, strand = 1),type='gene',id=acc2id,qualifiers={'locus_tag':[acc4id],'color':[10]})]

#Add a body - using bp as the scale length here.
body = BasicChromosome.AnnotatedChromosomeSegment(1000000,feats)
body.scale = 1000000
body.fill_color = fill
scale.add(body)



# This chromosome is done
chr_diagram.add(scale)


chr_diagram.draw(out, sys.argv[-1].split('/')[-1].replace('.pdf',''))
