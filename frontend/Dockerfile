# frontend/Dockerfile

# Usamos una imagen de Node ligera
FROM node:18-alpine

# Directorio de trabajo
WORKDIR /app

# Copiamos los archivos de definición de dependencias primero
# Esto aprovecha la caché de Docker: si no cambian las dependencias, no se reinstalan
COPY package.json package-lock.json ./

# Instalamos las dependencias
RUN npm install

# Copiamos el resto del código
COPY . .

# Exponemos el puerto 3000 (estándar de React)
EXPOSE 3000

# Comando por defecto para desarrollo
CMD ["npm", "start"]