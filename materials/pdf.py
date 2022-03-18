from fpdf import FPDF, HTMLMixin

from materials.models import *

data = (
    ("#", "Designation", "Qté", "Marque", "Etat", "Mode acquisition", "Année", "Observation"),
)
class PDF(FPDF, HTMLMixin):
    pass

def generate(request):
    sites = Site.objects.all()
    pdf = PDF()

    pdf.set_font("Times", size=10)
    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4  # distribute content evenly
    pdf.set_font_size(16)
    for site in sites :
        entrepots = Entrepots.objects.filter(site__pk=site.id)
        for ent in entrepots :
            stocks = ent.stock_set.all()
            pdf.add_page()

            rowspan = stocks.count()
            print(rowspan)
            if stocks :
                for i,stock in enumerate(stocks):
                    pdf.write_html(
                        f"""<table border="1"><thead><tr>
                        <th width="14%">{data[0][0]}</th>
                        <th width="14%">{data[0][1]}</th>
                        <th width="14%">{data[0][2]}</th>
                        <th width="14%">{data[0][3]}</th>
                        <th width="14%">{data[0][4]}</th>
                        <th width="14%">{data[0][5]}</th>
                        <th >{data[0][6]}</th>
                        <th >{data[0][7]}</th>
                    </tr></thead><tbody><tr>
                        <td>{'</td><td>'.join(str(i))}</td>
                    </tr><tr>
                        <td>{'</td><td>'.join(stock.materiel.name)}</td>
                    </tr><tr>
                        <td>{'</td><td>'.join(str(stock.qte))}</td>
                    </tr><tr>
                        <td>{'</td><td>'.join(stock.materiel.name)}</td>
                    </tr><tr>
                        <td>{'</td><td>'.join(str(stock.materiel.fabricat_year))}</td>
                    </tr><tr>
                        <td>{'</td><td>'.join(str(stock.qte))}</td>
                    </tr><tr>
                        <td>{'</td><td>'.join(str(stock.qte))}</td>
                    </tr><tr>
                        <td>{'</td><td>'.join(str(stock.qte))}</td>
                    </tr>
                    </tbody></table>""",
                        table_line_separators=True,
                    )
    pdf.output('table_html.pdf')