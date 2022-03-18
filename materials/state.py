import io

from django.shortcuts import render

from .forms import SearchForm
from .models import *
from django.db.models import Avg, Count, Min, Sum
from django.views.generic.detail import SingleObjectMixin
from io import BytesIO
from django.http import HttpResponse, FileResponse
from fpdf import FPDF, HTMLMixin
import base64

title = "PATRIMONE \n"
w = [22, 10, 40, 36, 18, 14, 13, 15, 20, 20, 12, 15, 17, 17, 15];  # largeur des cellules
largeur = w[0] + w[1] + w[2] + w[3] + w[4] + w[5] + w[6] + w[7] + w[8] + w[9] + w[10] + w[11] + w[12] + w[13] + w[14];
h = 5;  # hauteur des cellules
h2 = 8;
h3 = 9;


class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)

    def TraitHorizontal(self, largeur, hauteur):
        global w
        self.Cell(largeur, hauteur, '', 'B', 0, 'R')
        self.Ln();

    def PointsVerticaux(self, border, position, hauteur):
        self.Cell(0.1, hauteur, '', border, 0, position);

    def CelluleTitreLigneHorizontal(self, border, border_sous_titre, hauteur, align, align2,
                                    pret, eff,
                                    mttPrete, interet, fraisG, assurance,
                                    montARemb, montRemb, ratio, intGenere, fraisGPlusInt,
                                    resteARecouvrer, intARecouvrer,
                                    style, taille, armee=[], grade=[]):
        global w;
        self.SetLineWidth(0.2);
        self.SetFont('Arial', 'B', taille);
        self.Cell(w[0], hauteur, pret, border, 0, 'L');
        self.Cell(w[1], hauteur, eff, border, 0, align);
        self.SetFont('Arial', style, taille);

        n = len(armee);
        if (n > 0):
            for i in range(0, n):
                self.Cell((w[2] / n), hauteur, armee[i], border_sous_titre, 0, align2);
        else:
            self.Cell((w[2]), hauteur, '', border, 0, align);

        t = len(grade);
        if (t > 0):
            for i in range(0, t):
                self.Cell((w[3] / t), hauteur, grade[i], border_sous_titre, 0, align2);
        else:
            self.Cell((w[3]), hauteur, '', border, 0, align);

        self.SetLineWidth(0.4);
        self.Cell(w[4], hauteur, mttPrete, border, 0, align2);
        self.Cell(w[5], hauteur, interet, border, 0, align2);
        self.Cell(w[6], hauteur, fraisG, border, 0, align2);
        self.Cell(w[7], hauteur, assurance, border, 0, align2);
        self.Cell(w[8], hauteur, montARemb, border, 0, align2);
        self.Cell(w[9], hauteur, montRemb, border, 0, align2);
        self.Cell(w[10], hauteur, ratio, border, 0, align2);
        self.Cell(w[11], hauteur, intGenere, border, 0, align2);
        self.Cell(w[12], hauteur, fraisGPlusInt, border, 0, align2);
        self.Cell(w[13], hauteur, resteARecouvrer, border, 0, align2);
        self.Cell(w[14], hauteur, intARecouvrer, border, 0, align2);
        # self.SetLineWidth(0.4);
        self.PointsVerticaux('R', 'R', hauteur);
        self.Ln();

    def CelluleTitreVertical(self, border, pret, eff, armee, effArmee, grade,
                             effGrade, mttPrete, interet, fraisG, assurance,
                             montARemb, montRemb, ratio, intGenere, fraisGPlusInt,
                             resteARecouvrer, intARecouvrer):
        global w;
        global h3;
        self.SetLineWidth(0.2);
        self.SetFont('Arial', 'B', 8);
        self.Cell(w[0], h3, pret, border, 0, 'L');
        self.SetFont('Arial', '', 8);
        self.Cell(w[1], h3, eff, border, 0, 'R');
        self.SetFont('Arial', 'B', 8);
        # self.SetLineWidth(0.1);
        self.Cell((w[2] / 5) * 2, h3, armee, 1, 0, 'L');
        self.SetFont('Arial', '', 8);
        self.Cell((w[2] / 5) * 3, h3, effArmee, 1, 0, 'R');
        self.SetFont('Arial', 'B', 8);

        self.Cell((w[3] / 2), h3, grade, 1, 0, 'L');
        self.SetFont('Arial', '', 8);
        self.Cell((w[3] / 2), h3, effGrade, 1, 0, 'R');
        self.SetLineWidth(0.4);
        self.Cell(w[4], h3, mttPrete, border, 0, 'R');
        self.Cell(w[5], h3, interet, border, 0, 'R');
        self.Cell(w[6], h3, fraisG, border, 0, 'R');
        self.Cell(w[7], h3, assurance, border, 0, 'R');
        self.Cell(w[8], h3, montARemb, border, 0, 'R');
        self.Cell(w[9], h3, montRemb, border, 0, 'R');
        self.Cell(w[10], h3, ratio, border, 0, 'R');
        self.Cell(w[11], h3, intGenere, border, 0, 'R');
        self.Cell(w[12], h3, fraisGPlusInt, border, 0, 'R');
        self.Cell(w[13], h3, resteARecouvrer, border, 0, 'R');
        self.Cell(w[14], h3, intARecouvrer, border, 0, 'R');
        self.SetLineWidth(0.4);
        self.PointsVerticaux('R', 'R');
        self.Ln();

    def CelluleTitreHorizontal(self, border, pret, eff,
                               mttPrete, interet, fraisG, assurance, montARemb, montRemb,
                               ratio, intGenere, fraisGPlusInt, resteARecouvrer, intARecouvrer, style,
                               armee=[], grade=[], ):
        global w;
        global h3;
        # global diviseur;
        self.SetLineWidth(0.2);
        self.SetFont('Arial', 'B', 7.5);
        self.Cell(w[0], h3, pret, border, 0, 'L');
        self.SetFont('Arial', '', 7.5);
        self.Cell(w[1], h3, eff, border, 0, 'R');
        self.SetFont('Arial', style, 7.5);

        n = len(armee);
        for i in range(0, n):
            self.Cell((w[2] / n), h3, armee[i], 1, 0, 'L');

        t = len(grade);
        for i in range(0, t):
            self.Cell((w[3] / t), h3, grade[i], 1, 0, 'L');

        self.SetLineWidth(0.4);
        self.Cell(w[4], h3, mttPrete, border, 0, 'R');
        self.Cell(w[5], h3, interet, border, 0, 'R');
        self.Cell(w[6], h3, fraisG, border, 0, 'R');
        self.Cell(w[7], h3, assurance, border, 0, 'R');
        self.Cell(w[8], h3, montARemb, border, 0, 'R');
        self.Cell(w[9], h3, montRemb, border, 0, 'R');
        self.Cell(w[10], h3, ratio, border, 0, 'R');
        self.Cell(w[11], h3, intGenere, border, 0, 'R');
        self.Cell(w[12], h3, fraisGPlusInt, border, 0, 'R');
        self.Cell(w[13], h3, resteARecouvrer, border, 0, 'R');
        self.Cell(w[14], h3, intARecouvrer, border, 0, 'R');
        self.SetLineWidth(0.4);
        self.PointsVerticaux('R', 'R');
        self.Ln();

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def pdf_datakar(request):
    sites = Site.objects.all()
    pdf = PDF()

    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    for site in sites:
        title = "PATRIMONE " + site.libelle
        print(title)
        pdf.set_title(title)
        for i in range(1, 41):
            pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
    pdf.output('tpop.pdf', 'F')


def pdf_par_site(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    pdf = FPDF(orientation='L', format='A4', unit='in')
    # Add new page. Without this you cannot create the document.

    # Remember to always put one of these at least once.
    pdf.set_font('Times', '', 10.0)
    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin

    # Set column width to 1/4 of effective page width to distribute content
    # evenly across table and page
    col_width = epw / 9

    # Since we do not need to draw lines anymore, there is no need to separate
    # headers from data matrix.
    sites = Site.objects.all()

    # Document title centered, 'B'old, 14 pt
    # ftotal =
    for site in sites:
        entrepots = Entrepots.objects.filter(site__pk=site.id)
        for ent in entrepots:
            #print(ent)
            th = pdf.font_size
            pdf.add_page()
            stocks = ent.stock_set.all()
            pdf.set_font('Times', 'B', 14.0)
            pdf.image('/home/requi/inventory/static/cork/assets/img/logo_ditt.jpg', w=1.5, h=1.5)
            pdf.set_xy(3, 1)
            pdf.multi_cell(epw / 2, 0.3, "PATRIMONE \nSITE " + site.libelle, align='C', border=1)
            pdf.set_xy(9.6, 0.4)
            pdf.image('/home/requi/inventory/static/cork/assets/img/logo_ditt.jpg', w=1.5, h=1.5)
            pdf.set_font('Times', 'B', 10.0)
            pdf.ln(0.1)

            pdf.cell(epw, 0.0, ent.libelle, align='C')

            pdf.ln(0.1)
            # pdf.ln(2 * th)
            pdf.cell(col_width / 4, 2 * th, "ID", border=1, align='C')
            pdf.cell(2.5 * col_width, 2 * th, "Désignation", border=1, align='C')
            pdf.cell(col_width / 2, 2 * th, "Qté", border=1, align='C')
            pdf.cell(col_width, 2 * th, "Marque", border=1, align='C')
            pdf.cell(col_width / 1.5, 2 * th, "Etat", border=1, align='C')
            pdf.cell(col_width, 2 * th, "Mode acquisition", border=1, align='C')
            pdf.cell(col_width / 2.5, 2 * th, "Année", border=1, align='C')
            pdf.cell(col_width * 2, 2 * th, "Observation", border=1, align='C')

            pdf.ln(2 * th)
            total = 0
            for i, stock in enumerate(stocks):
                # Text height is the same as current font size
                # stocks = list(stock)
                i += 1
                total += int(stock.qte)
                print(th)
                pdf.cell(col_width / 4, 2 * th, str(i), border=1, align='C')
                pdf.cell(2.5 * col_width, 2 * th, str(stock.materiel.name), border=1, align='L')
                pdf.cell(col_width / 2, 2 * th, str(stock.qte), border=1, align='C')
                pdf.cell(col_width, 2 * th,
                         stock.materiel.frabriquant.libelle if stock.materiel.frabriquant is not None else "", border=1,
                         align='C')
                pdf.cell(col_width / 1.5, 2 * th, str("Bon"), border=1, align='C')
                pdf.cell(col_width, 2 * th, str(stock.materiel.mode_acquisition.libelle), border=1, align='C')
                pdf.cell(col_width / 2.5, 2 * th, str(stock.materiel.fabricat_year), border=1, align='C')
                pdf.cell(col_width * 2, 2 * th, str(), border=1, align='C')

                pdf.ln(2 * th)

            pdf.cell(2.75 * col_width, 2 * th, "TOTAL MATERIEL", border=1, align='C')
            pdf.cell(col_width / 2, 2 * th, str(total), border=1, align='C')

    pdf.ln(2 * th)
    # pdf.output('table-.pdf', dest="F")
    byte_string = pdf.output(dest="S")
    stream = BytesIO(byte_string)
    response = HttpResponse(stream)
    response['Content-Type'] = 'application/pdf'

    return response


def pdf_filter(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    pdf = FPDF(orientation='L', format='A4', unit='in')
    # Add new page. Without this you cannot create the document.

    # Remember to always put one of these at least once.
    pdf.set_font('Times', '', 10.0)
    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin

    # Set column width to 1/4 of effective page width to distribute content
    # evenly across table and page
    col_width = epw / 9

    # Since we do not need to draw lines anymore, there is no need to separate
    # headers from data matrix.
    sites = Site.objects.all()

    # Document title centered, 'B'old, 14 pt
    # ftotal =

    if request.POST or request.GET:

        site = request.POST.get("site")
        bureau = request.POST.get("bureau")
        categorie_materiel = request.POST.get("categorie_materiel")
        materiel = request.POST.get("materiel")

        if request.POST.get("site"):
            sites = Site.objects.filter(pk=site)

        else:
            sites = Site.objects.all()
    th = 0
    ##pdf.add_page()
    for site in sites:

        entrepots = Entrepots.objects.filter(site__pk=site.id)
        if entrepots:
            if request.POST.get("bureau"):
                print(request.POST.get("bureau"))
                entrepots = Entrepots.objects.filter(site__pk=site.id).filter(pk=bureau)
            print(entrepots)
            for ent in entrepots:
                #print(ent)
                th = pdf.font_size
                pdf.add_page()
                stocks = ent.stock_set.all()
                pdf.set_font('Times', 'B', 14.0)
                pdf.image('/home/requi/inventory/static/cork/assets/img/logo_ditt.jpg', w=1.5, h=1.5)
                pdf.set_xy(3, 1)
                pdf.multi_cell(epw / 2, 0.3, "PATRIMONE \nSITE " + site.libelle, align='C', border=1)
                pdf.set_xy(9.6, 0.4)
                pdf.image('/home/requi/inventory/static/cork/assets/img/logo_ditt.jpg', w=1.5, h=1.5)
                pdf.set_font('Times', 'B', 10.0)
                pdf.ln(0.1)

                pdf.cell(epw, 0.0, ent.libelle, align='C')

                pdf.ln(0.1)
                # pdf.ln(2 * th)
                pdf.cell(col_width / 4, 2 * th, "ID", border=1, align='C')
                pdf.cell(2.5 * col_width, 2 * th, "Désignation", border=1, align='C')
                pdf.cell(col_width / 2, 2 * th, "Qté", border=1, align='C')
                pdf.cell(col_width, 2 * th, "Marque", border=1, align='C')
                pdf.cell(col_width / 1.5, 2 * th, "Etat", border=1, align='C')
                pdf.cell(col_width, 2 * th, "Mode acquisition", border=1, align='C')
                pdf.cell(col_width / 2.5, 2 * th, "Année", border=1, align='C')
                pdf.cell(col_width * 2, 2 * th, "Observation", border=1, align='C')

                pdf.ln(2 * th)
                total = 0
                for i, stock in enumerate(stocks):
                    # Text height is the same as current font size
                    # stocks = list(stock)
                    i += 1
                    total += int(stock.qte)
                    print(th)
                    pdf.cell(col_width / 4, 2 * th, str(i), border=1, align='C')
                    pdf.cell(2.5 * col_width, 2 * th, str(stock.materiel.name), border=1, align='L')
                    pdf.cell(col_width / 2, 2 * th, str(stock.qte), border=1, align='C')
                    pdf.cell(col_width, 2 * th,
                             stock.materiel.frabriquant.libelle if stock.materiel.frabriquant is not None else "",
                             border=1, align='C')
                    pdf.cell(col_width / 1.5, 2 * th, str("Bon"), border=1, align='C')
                    pdf.cell(col_width, 2 * th, str(stock.materiel.mode_acquisition.libelle), border=1, align='C')
                    pdf.cell(col_width / 2.5, 2 * th, str(stock.materiel.fabricat_year), border=1, align='C')
                    pdf.cell(col_width * 2, 2 * th, str(), border=1, align='C')

                    pdf.ln(2 * th)

                pdf.cell(2.75 * col_width, 2 * th, "TOTAL MATERIEL", border=1, align='C')
                pdf.cell(col_width / 2, 2 * th, str(total), border=1, align='C')
        else:
            form = SearchForm(request.POST or None, request.FILES or None, )
            return render(request, "rakuda/etat/etat.html", locals())

    pdf.ln(2 * th)
    # pdf.output('table-.pdf', dest="F")
    byte_string = pdf.output(dest="S")
    stream = BytesIO(byte_string)
    response = HttpResponse(stream)
    response['Content-Type'] = 'application/pdf'

    return response


def cat_pdf_filter(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    pdf = FPDF(orientation='L', format='A4', unit='in')
    # Add new page. Without this you cannot create the document.

    # Remember to always put one of these at least once.
    pdf.set_font('Times', '', 10.0)
    # Effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin

    # Set column width to 1/4 of effective page width to distribute content
    # evenly across table and page
    col_width = epw / 9

    # Since we do not need to draw lines anymore, there is no need to separate
    # headers from data matrix.
    sites = Site.objects.all()

    # Document title centered, 'B'old, 14 pt
    # ftotal =

    if request.POST or request.GET:

        categorie_materiel = request.POST.get("categorie_materiel")
        materiel = request.POST.get("materiel")

        if request.POST.get("categorie_materiel"):
            sites = Site.objects.filter(pk=categorie_materiel)

        else:
            sites = Site.objects.all()
    th = 0
    ##pdf.add_page()
    for site in sites:

        entrepots = Entrepots.objects.filter(site__pk=site.id)
        if entrepots:
            if request.POST.get("bureau"):
                print(request.POST.get("bureau"))
                entrepots = Entrepots.objects.filter(site__pk=site.id).filter(pk=bureau)
            print(entrepots)
            for ent in entrepots:
                print(ent)
                th = pdf.font_size
                pdf.add_page()
                stocks = ent.stock_set.all()
                pdf.set_font('Times', 'B', 14.0)
                pdf.image('static/cork/assets/img/logo_ditt.jpg', w=1.5, h=1.5)
                pdf.set_xy(3, 1)
                pdf.multi_cell(epw / 2, 0.3, "PATRIMONE \nSITE " + site.libelle, align='C', border=1)
                pdf.set_xy(9.6, 0.4)
                pdf.image('static/cork/assets/img/logo_ditt.jpg', w=1.5, h=1.5)
                pdf.set_font('Times', 'B', 10.0)
                pdf.ln(0.1)

                pdf.cell(epw, 0.0, ent.libelle, align='C')

                pdf.ln(0.1)
                # pdf.ln(2 * th)
                pdf.cell(col_width / 4, 2 * th, "ID", border=1, align='C')
                pdf.cell(2.5 * col_width, 2 * th, "Désignation", border=1, align='C')
                pdf.cell(col_width / 2, 2 * th, "Qté", border=1, align='C')
                pdf.cell(col_width, 2 * th, "Marque", border=1, align='C')
                pdf.cell(col_width / 1.5, 2 * th, "Etat", border=1, align='C')
                pdf.cell(col_width, 2 * th, "Mode acquisition", border=1, align='C')
                pdf.cell(col_width / 2.5, 2 * th, "Année", border=1, align='C')
                pdf.cell(col_width * 2, 2 * th, "Observation", border=1, align='C')

                pdf.ln(2 * th)
                total = 0
                for i, stock in enumerate(stocks):
                    # Text height is the same as current font size
                    # stocks = list(stock)
                    i += 1
                    total += int(stock.qte)
                    print(th)
                    pdf.cell(col_width / 4, 2 * th, str(i), border=1, align='C')
                    pdf.cell(2.5 * col_width, 2 * th, str(stock.materiel.name), border=1, align='L')
                    pdf.cell(col_width / 2, 2 * th, str(stock.qte), border=1, align='C')
                    pdf.cell(col_width, 2 * th,
                             stock.materiel.frabriquant.libelle if stock.materiel.frabriquant is not None else "",
                             border=1, align='C')
                    pdf.cell(col_width / 1.5, 2 * th, str("Bon"), border=1, align='C')
                    pdf.cell(col_width, 2 * th, str(stock.materiel.mode_acquisition.libelle), border=1, align='C')
                    pdf.cell(col_width / 2.5, 2 * th, str(stock.materiel.fabricat_year), border=1, align='C')
                    pdf.cell(col_width * 2, 2 * th, str(), border=1, align='C')

                    pdf.ln(2 * th)

                pdf.cell(2.75 * col_width, 2 * th, "TOTAL MATERIEL", border=1, align='C')
                pdf.cell(col_width / 2, 2 * th, str(total), border=1, align='C')
        else:
            form = SearchForm(request.POST or None, request.FILES or None, )
            return render(request, "rakuda/etat/etat.html", locals())

    pdf.ln(2 * th)
    # pdf.output('table-.pdf', dest="F")
    byte_string = pdf.output(dest="S")
    stream = BytesIO(byte_string)
    response = HttpResponse(stream)
    response['Content-Type'] = 'application/pdf'

    return response
