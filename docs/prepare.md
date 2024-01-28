# Prepare a PDF form

The most common tool to create a PDF form is Adobe Acrobat. A tutorial can be found 
[here](https://helpx.adobe.com/acrobat/using/creating-distributing-pdf-forms.html). 
There are other free alternatives like [DocFly](https://www.docfly.com/) that support similar functionalities.

Given a PDF that's not a form yet, PyPDFForm also supports 
creating a subset of PDF form widgets on it through coding.

This section of the documentation will use 
[this PDF](https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf) as an example.

This section of the documentation requires a basic understanding of [the PDF coordinate system](coordinate.md).

## Create a text field widget

A text field widget can be created by downloading the PDF and running the following snippet:

```python
from PyPDFForm import PdfWrapper

new_form = PdfWrapper("dummy.pdf").create_widget(
    widget_type="text",
    name="new_text_field_widget",
    page_number=1,
    x=57,
    y=700,
    width=120,
    height=40,
    max_length=5,
    font="Courier",
    font_size=15,
    font_color=(1, 0, 0)
)

with open("output.pdf", "wb+") as output:
    output.write(new_form.read())
```

## Create a checkbox widget

A checkbox widget can be created using the same method with some changes to the parameters:

```python
from PyPDFForm import PdfWrapper

new_form = PdfWrapper("dummy.pdf").create_widget(
    widget_type="checkbox",
    name="new_checkbox_widget",
    page_number=1,
    x=57,
    y=700,
    size=30,
    button_style="check"
)

with open("output.pdf", "wb+") as output:
    output.write(new_form.read())
```

The `button_style` parameter currently supports three options: `check`, `circle`, and `cross`.
