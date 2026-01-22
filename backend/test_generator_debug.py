#!/usr/bin/env python3
"""Script de depuración para el generador de Braille."""

import sys
import traceback
from io import BytesIO

print("=" * 60)
print("DEBUGGING BRAILLE GENERATOR")
print("=" * 60)

# Test 1: Translator
print("\n[1] Testing text_to_braille...")
try:
    from app.api.services.translator import text_to_braille
    result = text_to_braille('Hola')
    print(f"    ✓ SUCCESS: {result}")
except Exception as e:
    print(f"    ✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 2: PIL/Pillow
print("\n[2] Testing PIL/Pillow...")
try:
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (100, 100), 'white')
    draw = ImageDraw.Draw(img)
    draw.ellipse([10, 10, 20, 20], fill='black')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    print(f"    ✓ SUCCESS: PIL working, generated {len(buffer.getvalue())} bytes")
except Exception as e:
    print(f"    ✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 3: BrailleImageGenerator
print("\n[3] Testing BrailleImageGenerator.__init__...")
try:
    from app.api.services.generator import BrailleImageGenerator
    gen = BrailleImageGenerator()
    print(f"    ✓ SUCCESS: Created generator with cell_width={gen.cell_width}, cell_height={gen.cell_height}")
except Exception as e:
    print(f"    ✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 4: generate_image method
print("\n[4] Testing BrailleImageGenerator.generate_image()...")
try:
    buffer = gen.generate_image("Hola", include_text=True)
    size = len(buffer.getvalue())
    print(f"    ✓ SUCCESS: Generated image with {size} bytes")
except Exception as e:
    print(f"    ✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 5: ReportLab
print("\n[5] Testing ReportLab...")
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawString(100, 750, "Test")
    c.save()
    size = len(buffer.getvalue())
    print(f"    ✓ SUCCESS: ReportLab working, generated {size} bytes")
except Exception as e:
    print(f"    ✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 6: BraillePDFGenerator
print("\n[6] Testing BraillePDFGenerator...")
try:
    from app.api.services.generator import BraillePDFGenerator
    gen_pdf = BraillePDFGenerator()
    buffer = gen_pdf.generate_pdf("Hola", "Test PDF")
    size = len(buffer.getvalue())
    print(f"    ✓ SUCCESS: Generated PDF with {size} bytes")
except Exception as e:
    print(f"    ✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 7: generate_braille_pdf function
print("\n[7] Testing generate_braille_pdf()...")
try:
    from app.api.services.generator import generate_braille_pdf
    buffer = generate_braille_pdf("Hola", "Test")
    size = len(buffer.getvalue())
    print(f"    ✓ SUCCESS: Generated PDF with {size} bytes")
except Exception as e:
    print(f"    ✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 8: generate_braille_image function
print("\n[8] Testing generate_braille_image()...")
try:
    from app.api.services.generator import generate_braille_image
    buffer = generate_braille_image("Hola", True)
    size = len(buffer.getvalue())
    print(f"    ✓ SUCCESS: Generated image with {size} bytes")
except Exception as e:
    print(f"    ✗ ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
