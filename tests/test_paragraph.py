# -*- coding: utf-8 -*-
# pylint: disable=line-too-long

import os

from PyPDFForm import PdfWrapper


def test_paragraph_y_coordinate(sample_template_with_paragraph, pdf_samples, request):
    expected_path = os.path.join(
        pdf_samples, "paragraph", "test_paragraph_y_coordinate.pdf"
    )
    with open(expected_path, "rb+") as f:
        obj = PdfWrapper(sample_template_with_paragraph).fill(
            {"paragraph_1": "test paragraph"}
        )

        request.config.results["expected_path"] = expected_path
        request.config.results["stream"] = obj.read()
        assert len(obj.read()) == len(obj.read())
        assert obj.read() == obj.read()

        expected = f.read()

        assert len(obj.read()) == len(expected)
        assert obj.read() == expected


def test_paragraph_auto_wrap(sample_template_with_paragraph, pdf_samples, request):
    expected_path = os.path.join(
        pdf_samples, "paragraph", "test_paragraph_auto_wrap.pdf"
    )
    with open(expected_path, "rb+") as f:
        obj = PdfWrapper(sample_template_with_paragraph).fill(
            {
                "paragraph_1": "t xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx t"
            }
        )

        request.config.results["expected_path"] = expected_path
        request.config.results["stream"] = obj.read()
        assert len(obj.read()) == len(obj.read())
        assert obj.read() == obj.read()

        expected = f.read()

        assert len(obj.read()) == len(expected)
        assert obj.read() == expected
        assert obj.widgets["paragraph_1"].text_wrap_length is not None


def test_paragraph_auto_font(
    sample_template_with_paragraph_auto_font, pdf_samples, request
):
    expected_path = os.path.join(
        pdf_samples, "paragraph", "test_paragraph_auto_font.pdf"
    )
    with open(expected_path, "rb+") as f:
        obj = PdfWrapper(sample_template_with_paragraph_auto_font).fill(
            {"paragraph": "test paragraph"}
        )

        request.config.results["expected_path"] = expected_path
        request.config.results["stream"] = obj.read()
        assert len(obj.read()) == len(obj.read())
        assert obj.read() == obj.read()

        expected = f.read()

        if os.name != "nt":
            assert len(obj.read()) == len(expected)
            assert obj.read() == expected


def test_paragraph_auto_font_auto_wrap(
    sample_template_with_paragraph_auto_font, pdf_samples, request
):
    expected_path = os.path.join(
        pdf_samples, "paragraph", "test_paragraph_auto_font_auto_wrap.pdf"
    )
    with open(expected_path, "rb+") as f:
        obj = PdfWrapper(sample_template_with_paragraph_auto_font).fill(
            {
                "paragraph": "t xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx t"
            }
        )

        request.config.results["expected_path"] = expected_path
        request.config.results["stream"] = obj.read()
        assert len(obj.read()) == len(obj.read())
        assert obj.read() == obj.read()

        expected = f.read()

        if os.name != "nt":
            assert len(obj.read()) == len(expected)
            assert obj.read() == expected
            assert obj.widgets["paragraph"].text_wrap_length is not None


def test_fill_sejda_complex(sejda_template_complex, pdf_samples, request):
    expected_path = os.path.join(
        pdf_samples, "paragraph", "sample_filled_sejda_complex.pdf"
    )
    with open(expected_path, "rb+") as f:
        obj = PdfWrapper(sejda_template_complex).fill(
            {
                "checkbox": True,
                "radio": 0,
                "dropdown_font_auto_left": 0,
                "dropdown_font_auto_center": 1,
                "dropdown_font_auto_right": 2,
                "dropdown_font_ten_left": 0,
                "dropdown_font_ten_center": 1,
                "dropdown_font_ten_right": 2,
                "paragraph_font_auto_left": "paragraph_font_auto_left",
                "paragraph_font_auto_center": "paragraph_font_auto_center",
                "paragraph_font_auto_right": "paragraph_font_auto_right",
                "paragraph_font_ten_left": "paragraph_font_ten_left",
                "paragraph_font_ten_center": "paragraph_font_ten_center",
                "paragraph_font_ten_right": "paragraph_font_ten_right",
                "text__font_auto_left": "test text",
                "text_font_auto_center": "test text",
                "text_font_auto_right": "test text",
                "text_font_ten_left": "text_font_ten_left",
                "text_font_ten_center": "text_font_ten_center",
                "text_font_ten_right": "text_font_ten_right",
            }
        )

        request.config.results["expected_path"] = expected_path
        request.config.results["stream"] = obj.read()
        assert len(obj.read()) == len(obj.read())
        assert obj.read() == obj.read()

        expected = f.read()

        assert len(obj.read()) == len(expected)
        assert obj.read() == expected


def test_fill_sejda_complex_not_render_widgets(
    sejda_template_complex, pdf_samples, request
):
    expected_path = os.path.join(
        pdf_samples, "paragraph", "test_fill_sejda_complex_not_render_widgets.pdf"
    )
    with open(expected_path, "rb+") as f:
        obj = PdfWrapper(sejda_template_complex, render_widgets=False).fill(
            {
                "checkbox": True,
                "radio": 0,
                "dropdown_font_auto_left": 0,
                "dropdown_font_auto_center": 1,
                "dropdown_font_auto_right": 2,
                "dropdown_font_ten_left": 0,
                "dropdown_font_ten_center": 1,
                "dropdown_font_ten_right": 2,
                "paragraph_font_auto_left": "paragraph_font_auto_left",
                "paragraph_font_auto_center": "paragraph_font_auto_center",
                "paragraph_font_auto_right": "paragraph_font_auto_right",
                "paragraph_font_ten_left": "paragraph_font_ten_left",
                "paragraph_font_ten_center": "paragraph_font_ten_center",
                "paragraph_font_ten_right": "paragraph_font_ten_right",
                "text__font_auto_left": "test text",
                "text_font_auto_center": "test text",
                "text_font_auto_right": "test text",
                "text_font_ten_left": "text_font_ten_left",
                "text_font_ten_center": "text_font_ten_center",
                "text_font_ten_right": "text_font_ten_right",
            }
        )

        request.config.results["expected_path"] = expected_path
        request.config.results["stream"] = obj.read()
        assert len(obj.read()) == len(obj.read())
        assert obj.read() == obj.read()

        expected = f.read()

        assert len(obj.read()) == len(expected)
        assert obj.read() == expected


def test_fill_sejda_complex_not_render_some_widgets(
    sejda_template_complex, pdf_samples, request
):
    expected_path = os.path.join(
        pdf_samples, "paragraph", "test_fill_sejda_complex_not_render_some_widgets.pdf"
    )
    with open(expected_path, "rb+") as f:
        obj = PdfWrapper(sejda_template_complex)

        obj.widgets["radio"].render_widget = False
        obj.widgets["dropdown_font_auto_center"].render_widget = False
        obj.widgets["dropdown_font_ten_center"].render_widget = False
        obj.widgets["paragraph_font_auto_center"].render_widget = False
        obj.widgets["paragraph_font_ten_center"].render_widget = False
        obj.widgets["text_font_auto_center"].render_widget = False
        obj.widgets["text_font_ten_center"].render_widget = False

        obj.fill(
            {
                "checkbox": True,
                "radio": 0,
                "dropdown_font_auto_left": 0,
                "dropdown_font_auto_center": 1,
                "dropdown_font_auto_right": 2,
                "dropdown_font_ten_left": 0,
                "dropdown_font_ten_center": 1,
                "dropdown_font_ten_right": 2,
                "paragraph_font_auto_left": "paragraph_font_auto_left",
                "paragraph_font_auto_center": "paragraph_font_auto_center",
                "paragraph_font_auto_right": "paragraph_font_auto_right",
                "paragraph_font_ten_left": "paragraph_font_ten_left",
                "paragraph_font_ten_center": "paragraph_font_ten_center",
                "paragraph_font_ten_right": "paragraph_font_ten_right",
                "text__font_auto_left": "test text",
                "text_font_auto_center": "test text",
                "text_font_auto_right": "test text",
                "text_font_ten_left": "text_font_ten_left",
                "text_font_ten_center": "text_font_ten_center",
                "text_font_ten_right": "text_font_ten_right",
            }
        )

        request.config.results["expected_path"] = expected_path
        request.config.results["stream"] = obj.read()
        assert len(obj.read()) == len(obj.read())
        assert obj.read() == obj.read()

        expected = f.read()

        assert len(obj.read()) == len(expected)
        assert obj.read() == expected


def test_sejda_complex_paragraph_multiple_line_alignment(
    sejda_template_complex, pdf_samples, request
):
    expected_path = os.path.join(
        pdf_samples,
        "paragraph",
        "sample_filled_sejda_complex_paragraph_multiple_line_alignment.pdf",
    )
    with open(expected_path, "rb+") as f:
        obj = PdfWrapper(sejda_template_complex).fill(
            {
                "paragraph_font_auto_left": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                "paragraph_font_auto_right": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                "paragraph_font_auto_center": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                "paragraph_font_ten_left": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                "paragraph_font_ten_right": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                "paragraph_font_ten_center": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
            }
        )

        request.config.results["expected_path"] = expected_path
        request.config.results["stream"] = obj.read()
        assert len(obj.read()) == len(obj.read())
        assert obj.read() == obj.read()

        expected = f.read()

        assert len(obj.read()) == len(expected)
        assert obj.read() == expected


def test_paragraph_complex(sample_template_paragraph_complex, pdf_samples, request):
    expected_path = os.path.join(pdf_samples, "paragraph", "test_paragraph_complex.pdf")
    with open(expected_path, "rb+") as f:
        obj = PdfWrapper(sample_template_paragraph_complex).fill(
            {
                "paragraph_font_auto_left": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                "paragraph_font_auto_right": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                "paragraph_font_auto_center": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                "paragraph_font_ten_left": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                "paragraph_font_ten_right": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                "paragraph_font_ten_center": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
            }
        )

        request.config.results["expected_path"] = expected_path
        request.config.results["stream"] = obj.read()
        assert len(obj.read()) == len(obj.read())
        assert obj.read() == obj.read()

        expected = f.read()

        if os.name != "nt":
            assert len(obj.read()) == len(expected)
            assert obj.read() == expected


def test_paragraph_max_length(
    sample_template_with_paragraph_max_length, pdf_samples, request
):
    expected_path = os.path.join(
        pdf_samples, "paragraph", "test_paragraph_max_length.pdf"
    )
    with open(expected_path, "rb+") as f:
        obj = PdfWrapper(sample_template_with_paragraph_max_length).fill(
            {
                "paragraph": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
            }
        )

        request.config.results["expected_path"] = expected_path
        request.config.results["stream"] = obj.read()
        assert len(obj.read()) == len(obj.read())
        assert obj.read() == obj.read()

        expected = f.read()

        if os.name != "nt":
            assert len(obj.read()) == len(expected)
            assert obj.read() == expected
