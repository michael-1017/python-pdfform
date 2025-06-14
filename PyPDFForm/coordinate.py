# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import List, Tuple, Union

from pypdf import PdfReader
from reportlab.pdfbase.pdfmetrics import stringWidth

from .constants import (COORDINATE_GRID_FONT_SIZE_MARGIN_RATIO, DEFAULT_FONT,
                        Rect)
from .middleware.text import Text
from .patterns import WIDGET_ALIGNMENT_PATTERNS
from .template import get_char_rect_width, is_text_multiline
from .utils import extract_widget_property, handle_color, stream_to_io
from .watermark import create_watermarks_and_draw, merge_watermarks_with_pdf


def get_draw_border_coordinates(widget: dict, shape: str) -> dict:
    result = {
        "x": float(widget[Rect][0]),
        "y": float(widget[Rect][1]),
        "width": abs(float(widget[Rect][0]) - float(widget[Rect][2])),
        "height": abs(float(widget[Rect][1]) - float(widget[Rect][3])),
    }

    if shape == "ellipse":
        width = abs(float(widget[Rect][0]) - float(widget[Rect][2]))
        height = abs(float(widget[Rect][1]) - float(widget[Rect][3]))

        width_mid = (float(widget[Rect][0]) + float(widget[Rect][2])) / 2
        height_mid = (float(widget[Rect][1]) + float(widget[Rect][3])) / 2

        less = min(width, height)

        result = {
            "x1": width_mid - less / 2,
            "y1": height_mid - less / 2,
            "x2": width_mid + less / 2,
            "y2": height_mid + less / 2,
        }
    elif shape == "line":
        result = {
            "src_x": float(widget[Rect][0]),
            "src_y": float(widget[Rect][1]),
            "dest_x": float(widget[Rect][2]),
            "dest_y": float(widget[Rect][1]),
        }

    return result


def get_draw_checkbox_radio_coordinates(
    widget: dict,
    widget_middleware: Text,
    border_width: int,
) -> Tuple[Union[float, int], Union[float, int]]:
    string_height = widget_middleware.font_size * 72 / 96
    width_mid_point = (float(widget[Rect][0]) + float(widget[Rect][2])) / 2
    half_widget_height = abs(float(widget[Rect][1]) - float(widget[Rect][3])) / 2

    return (
        width_mid_point
        - stringWidth(
            widget_middleware.value,
            widget_middleware.font,
            widget_middleware.font_size,
        )
        / 2,
        float(widget[Rect][1])
        + (half_widget_height - string_height / 2)
        + border_width / 2,
    )


def get_draw_image_coordinates_resolutions(
    widget: dict,
    preserve_aspect_ratio: bool,
    image_width: float,
    image_height: float,
) -> Tuple[float, float, float, float]:
    x = float(widget[Rect][0])
    y = float(widget[Rect][1])
    width = abs(float(widget[Rect][0]) - float(widget[Rect][2]))
    height = abs(float(widget[Rect][1]) - float(widget[Rect][3]))

    if preserve_aspect_ratio:
        ratio = max(image_width / width, image_height / height)

        new_width = image_width / ratio
        new_height = image_height / ratio

        x += abs(new_width - width) / 2
        y += abs(new_height - height) / 2

        width = new_width
        height = new_height

    return x, y, width, height


def calculate_text_coord_x(
    widget: dict,
    widget_middleware: Text,
    text_value: str,
    length: int,
    character_paddings: List[float],
) -> float:
    alignment = (
        extract_widget_property(widget, WIDGET_ALIGNMENT_PATTERNS, None, int) or 0
    )
    # Default to left boundary
    x = float(widget[Rect][0])

    if int(alignment) == 0:
        return x

    # Calculate the horizontal midpoint of the widget rectangle
    width_mid_point = (float(widget[Rect][0]) + float(widget[Rect][2])) / 2

    # Calculate the width of the entire string in points
    string_width = stringWidth(
        text_value,
        widget_middleware.font,
        widget_middleware.font_size,
    )

    # If comb formatting, adjust string width to include last character's right padding
    if widget_middleware.comb is True and length:
        string_width = character_paddings[-1] + stringWidth(
            text_value[-1],
            widget_middleware.font,
            widget_middleware.font_size,
        )

    if int(alignment) == 1:  # Center alignment
        # Center text by offsetting half the string width from the midpoint
        x = width_mid_point - string_width / 2
    elif int(alignment) == 2:  # Right alignment
        # Align text to the right edge minus the string width
        x = float(widget[Rect][2]) - string_width
        if length > 0 and widget_middleware.comb is True:
            # For comb fields, adjust further by half the difference between comb box width and last character width
            x -= (
                get_char_rect_width(widget, widget_middleware)
                - stringWidth(
                    text_value[-1],
                    widget_middleware.font,
                    widget_middleware.font_size,
                )
            ) / 2

    # Additional comb adjustment for center alignment
    if int(alignment) == 1 and widget_middleware.comb is True and length != 0:
        # Shift left by half the first character's padding
        x -= character_paddings[0] / 2
        if length % 2 == 0:
            # For even-length comb text, shift further left by half the first char width plus padding
            x -= (
                character_paddings[0]
                + stringWidth(
                    text_value[:1],
                    widget_middleware.font,
                    widget_middleware.font_size,
                )
                / 2
            )

    return x


def calculate_text_coord_y(widget: dict, widget_middleware: Text) -> float:
    # Convert font size to PDF points (font size is in pixels, 96 dpi to 72 dpi)
    string_height = widget_middleware.font_size * 96 / 72

    # Calculate vertical midpoint of the widget rectangle
    height_mid_point = (float(widget[Rect][1]) + float(widget[Rect][3])) / 2

    # Default y: vertically center the text baseline within the widget
    # This formula centers the text height around the vertical midpoint
    y = (height_mid_point - string_height / 2 + height_mid_point) / 2

    # If multiline, position baseline closer to the top edge for better appearance
    if is_text_multiline(widget):
        y = float(widget[Rect][3]) - string_height / 1.5

    return y


def get_draw_text_coordinates(
    widget: dict, widget_middleware: Text
) -> Tuple[Union[float, int], Union[float, int]]:
    # If preview mode, draw slightly above the top boundary for visibility
    if widget_middleware.preview:
        return (
            float(widget[Rect][0]),
            float(widget[Rect][3]) + 5,
        )

    # Prepare text value, respecting max length
    text_value = widget_middleware.value or ""
    length = (
        min(len(text_value), widget_middleware.max_length)
        if widget_middleware.max_length is not None
        else len(text_value)
    )
    text_value = text_value[:length]

    # Further trim text if wrapping is enabled
    if widget_middleware.text_wrap_length is not None:
        text_value = text_value[: widget_middleware.text_wrap_length]

    # Prepare character paddings for comb fields
    character_paddings = (
        widget_middleware.character_paddings[:length]
        if widget_middleware.character_paddings is not None
        else widget_middleware.character_paddings
    )

    # Calculate horizontal position based on alignment and comb settings
    x = calculate_text_coord_x(
        widget, widget_middleware, text_value, length, character_paddings
    )

    # Calculate vertical position based on font size and multiline
    y = calculate_text_coord_y(widget, widget_middleware)

    return x, y


def get_text_line_x_coordinates(
    widget: dict, widget_middleware: Text
) -> Union[List[float], None]:
    if (
        widget_middleware.text_wrap_length is not None
        and widget_middleware.text_lines is not None
        and len(widget_middleware.text_lines)
        and isinstance(widget_middleware.value, str)
        and len(widget_middleware.value) > widget_middleware.text_wrap_length
    ):
        result = []
        _widget = deepcopy(widget_middleware)
        for each in widget_middleware.text_lines:
            _widget.value = each
            _widget.text_wrap_length = None
            result.append(get_draw_text_coordinates(widget, _widget)[0])

        return result

    return None


def generate_coordinate_grid(
    pdf: bytes, color: Tuple[float, float, float], margin: float
) -> bytes:
    pdf_file = PdfReader(stream_to_io(pdf))
    lines_by_page = {}
    texts_by_page = {}
    watermarks = []

    for i, page in enumerate(pdf_file.pages):
        lines_by_page[i + 1] = []
        texts_by_page[i + 1] = []
        width = float(page.mediabox[2])
        height = float(page.mediabox[3])

        r, g, b = color

        current = margin
        while current < width:
            lines_by_page[i + 1].append(
                {
                    "src_x": current,
                    "src_y": 0,
                    "dest_x": current,
                    "dest_y": height,
                    "border_color": handle_color([r, g, b]),
                    "background_color": None,
                    "border_width": 1,
                    "dash_array": None,
                }
            )
            current += margin

        current = margin
        while current < height:
            lines_by_page[i + 1].append(
                {
                    "src_x": 0,
                    "src_y": current,
                    "dest_x": width,
                    "dest_y": current,
                    "border_color": handle_color([r, g, b]),
                    "background_color": None,
                    "border_width": 1,
                    "dash_array": None,
                }
            )
            current += margin

        x = margin
        while x < width:
            y = margin
            while y < height:
                value = f"({x}, {y})"
                font_size = margin * COORDINATE_GRID_FONT_SIZE_MARGIN_RATIO
                text = Text("new_coordinate", value)
                text.font = DEFAULT_FONT
                text.font_size = font_size
                text.font_color = color
                texts_by_page[i + 1].append(
                    {
                        "widget": text,
                        "x": x - stringWidth(value, DEFAULT_FONT, font_size),
                        "y": y - font_size,
                    }
                )
                y += margin
            x += margin

    for page, lines in lines_by_page.items():
        watermarks.append(
            create_watermarks_and_draw(pdf, page, "line", lines)[page - 1]
        )

    result = merge_watermarks_with_pdf(pdf, watermarks)
    watermarks = []
    for page, texts in texts_by_page.items():
        watermarks.append(
            create_watermarks_and_draw(pdf, page, "text", texts)[page - 1]
        )

    return merge_watermarks_with_pdf(result, watermarks)
