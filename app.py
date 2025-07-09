from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Base de datos en memoria
productos_db = []

# Menú para navegación
menu = '''
<div class="text-center space-x-4 mt-6">
  <a href="/productos" class="bg-green-500 text-white px-4 py-2 rounded">Agregar Producto</a>
  <a href="/productos/ver" class="bg-green-700 text-white px-4 py-2 rounded">Ver Productos</a>
  <a href="/inventario" class="bg-yellow-500 text-white px-4 py-2 rounded">Inventario</a>
  <a href="/clientes" class="bg-blue-600 text-white px-4 py-2 rounded">Clientes</a>
</div>
'''

def redirect_script():
    return """
<script>
  document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function() {
      setTimeout(function() {
        window.location.href = 'https://anamariadeveloper97.github.io/Energix/';
      }, 2000);
    });
  });
</script>
"""

@app.route('/')
def inicio():
    return render_template_string(f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>Inicio</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-lime-100 text-gray-800 font-sans">
  <div class="text-center py-10">
    <h1 class="text-4xl font-bold mb-4">Bienvenido a PURA FRUTA 🍓</h1>
    {menu}
  </div>
</body></html>
""")

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    if request.method == 'POST':
        nuevo = {
            'id': len(productos_db) + 1,
            'nombre': request.form['nombre'],
            'descripcion': request.form['descripcion'],
            'imagen': request.form['imagen']
        }
        productos_db.append(nuevo)
        return redirect('/productos/ver')

    return render_template_string(f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>Añadir Producto</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-green-100 text-gray-900 font-sans">
  <div class="container mx-auto py-10">
    <h1 class="text-3xl font-bold text-center mb-6">Añadir Producto 🍍</h1>
    <form method="POST" class="max-w-md mx-auto bg-white p-6 rounded shadow space-y-4">
      <input name="nombre" placeholder="Nombre del producto" required class="w-full px-4 py-2 border rounded">
      <input name="descripcion" placeholder="Descripción" required class="w-full px-4 py-2 border rounded">
      <input name="imagen" placeholder="URL de imagen" required class="w-full px-4 py-2 border rounded">
      <button type="submit" class="w-full bg-green-600 text-white py-2 rounded">Guardar</button>
    </form>
    {menu}
  </div>
</body></html>
""")

@app.route('/productos/ver')
def ver_productos():
    tabla = ""
    for p in productos_db:
        tabla += f"""
        <tr class="border-b">
          <td class="py-2 px-4">{p['nombre']}</td>
          <td class="py-2 px-4">{p['descripcion']}</td>
          <td class="py-2 px-4"><img src="{p['imagen']}" width="60"></td>
          <td class="py-2 px-4">
            <a href="/productos/editar/{p['id']}" class="text-blue-600">Editar</a> |
            <a href="/productos/eliminar/{p['id']}" class="text-red-600">Eliminar</a>
          </td>
        </tr>
        """
    return render_template_string(f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>Ver Productos</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-white text-gray-900 font-sans">
  <div class="container mx-auto py-10">
    <h1 class="text-3xl font-bold text-center mb-6">Productos Existentes 🧃</h1>
    <table class="table-auto w-full text-left bg-white border">
      <thead><tr class="bg-gray-100">
        <th class="py-2 px-4">Nombre</th>
        <th class="py-2 px-4">Descripción</th>
        <th class="py-2 px-4">Imagen</th>
        <th class="py-2 px-4">Acciones</th>
      </tr></thead>
      <tbody>{tabla}</tbody>
    </table>
    {menu}
  </div>
</body></html>
""")

@app.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    global productos_db
    productos_db = [p for p in productos_db if p['id'] != id]
    return redirect('/productos/ver')

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = next((p for p in productos_db if p['id'] == id), None)
    if not producto:
        return "Producto no encontrado", 404

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['descripcion'] = request.form['descripcion']
        producto['imagen'] = request.form['imagen']
        return redirect('/productos/ver')

    return render_template_string(f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>Editar Producto</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-green-50 text-gray-900 font-sans">
  <div class="container mx-auto py-10">
    <h1 class="text-3xl font-bold text-center mb-6">Editar Producto ✏️</h1>
    <form method="POST" class="max-w-md mx-auto bg-white p-6 rounded shadow space-y-4">
      <input name="nombre" value="{producto['nombre']}" required class="w-full px-4 py-2 border rounded">
      <input name="descripcion" value="{producto['descripcion']}" required class="w-full px-4 py-2 border rounded">
      <input name="imagen" value="{producto['imagen']}" required class="w-full px-4 py-2 border rounded">
      <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded">Actualizar</button>
    </form>
    {menu}
  </div>
</body></html>
""")

@app.route('/inventario')
def inventario():
    return render_template_string(f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>Inventario</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-yellow-50 text-gray-900 font-sans">
  <div class="container mx-auto py-10">
    <h1 class="text-3xl font-bold text-center mb-6">Registrar Venta 📦</h1>
    <form action="https://formspree.io/f/xldnyqzk" method="POST" class="max-w-md mx-auto bg-white p-6 rounded shadow space-y-4">
      <input name="producto" placeholder="Nombre del producto vendido" required class="w-full px-4 py-2 border rounded">
      <input name="cantidad" type="number" placeholder="Cantidad" required class="w-full px-4 py-2 border rounded">
      <input name="fecha" type="datetime-local" required class="w-full px-4 py-2 border rounded">
      <button type="submit" class="w-full bg-yellow-500 text-white py-2 rounded">Registrar</button>
    </form>
    {menu}
    {redirect_script()}
  </div>
</body></html>
""")

@app.route('/clientes')
def clientes():
    return render_template_string(f"""
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>Clientes</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-blue-100 text-gray-900 font-sans">
  <div class="container mx-auto py-10">
    <h1 class="text-3xl font-bold text-center mb-6">Registrar Cliente 🧍‍♀️🧍‍♂️</h1>
    <form action="https://formspree.io/f/mgvyjjkp" method="POST" class="max-w-md mx-auto bg-white p-6 rounded shadow space-y-4">
      <input name="nombre" placeholder="Nombre" required class="w-full px-4 py-2 border rounded">
      <input name="apellido" placeholder="Apellido" required class="w-full px-4 py-2 border rounded">
      <input name="correo" type="email" placeholder="Correo electrónico" required class="w-full px-4 py-2 border rounded">
      <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded">Registrar</button>
    </form>
    {menu}
    {redirect_script()}
  </div>
</body></html>
""")

if __name__ == '__main__':
    app.run(debug=True)

