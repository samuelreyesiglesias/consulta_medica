
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS SistemaSalud;
USE SistemaSalud;

-- Eliminar tablas si existen
DROP TABLE IF EXISTS Historial;
DROP TABLE IF EXISTS Cita;
DROP TABLE IF EXISTS Medico;
DROP TABLE IF EXISTS Especialidad;
DROP TABLE IF EXISTS Paciente;
DROP TABLE IF EXISTS Usuario;

-- Tabla de usuarios
CREATE TABLE Usuario (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  nombre_usuario VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  rol ENUM('admin', 'medico', 'recepcionista') NOT NULL
);

-- Tabla de pacientes
CREATE TABLE Paciente (
  id_paciente INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  fecha_nacimiento DATE NOT NULL,
  genero ENUM('masculino', 'femenino', 'otro') NOT NULL,
  telefono VARCHAR(20),
  direccion TEXT
);

-- Tabla de especialidades
CREATE TABLE Especialidad (
  id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL
);

-- Insertar especialidades básicas
INSERT INTO Especialidad (nombre) VALUES 
('Medicina General'),
('Pediatría'),
('Ginecología'),
('Cardiología'),
('Dermatología'),
('Neurología'),
('Ortopedia'),
('Oftalmología'),
('Otorrinolaringología'),
('Psiquiatría'),
('Endocrinología'),
('Gastroenterología'),
('Urología'),
('Nefrología'),
('Neumología'),
('Reumatología'),
('Oncología'),
('Traumatología'),
('Cirugía General'),
('Medicina Interna');

-- Tabla de médicos
CREATE TABLE Medico (
  id_medico INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  especialidad_id INT NOT NULL,
  FOREIGN KEY (especialidad_id) REFERENCES Especialidad(id_especialidad)
);

-- Tabla de citas
CREATE TABLE Cita (
  id_cita INT AUTO_INCREMENT PRIMARY KEY,
  paciente_id INT NOT NULL,
  medico_id INT NOT NULL,
  fecha_hora DATETIME NOT NULL,
  estado ENUM('pendiente', 'confirmada', 'cancelada', 'completada') NOT NULL,
  FOREIGN KEY (paciente_id) REFERENCES Paciente(id_paciente),
  FOREIGN KEY (medico_id) REFERENCES Medico(id_medico)
);

-- Tabla de historiales
CREATE TABLE Historial (
  id_historial INT AUTO_INCREMENT PRIMARY KEY,
  paciente_id INT NOT NULL,
  medico_id INT NOT NULL,
  fecha DATE NOT NULL,
  descripcion TEXT,
  FOREIGN KEY (paciente_id) REFERENCES Paciente(id_paciente),
  FOREIGN KEY (medico_id) REFERENCES Medico(id_medico)
);


-- Usuario administrador
INSERT INTO Usuario (nombre_usuario, password, rol)
VALUES ('admin1', 'admin123', 'admin');

-- Usuario recepcionista
INSERT INTO Usuario (nombre_usuario, password, rol)
VALUES ('recepcion1', 'recep123', 'recepcionista');

-- Usuario médico
INSERT INTO Usuario (nombre_usuario, password, rol)
VALUES ('medico1', 'medico123', 'medico');

-- Médico asociado (nombre debe coincidir con el usuario)
INSERT INTO Medico (nombre, especialidad_id)
VALUES ('medico1', 1);  -- Usa una especialidad válida, ej: Medicina General con id 1



-- Crear un nuevo usuario con rol médico Y agregarlo automáticamente como médico
-- Paso 1: Insertar en Usuario
INSERT INTO Usuario (nombre_usuario, password, rol) VALUES ('medico_auto', 'clave123', 'medico');

-- Paso 2: Obtener el nombre recién insertado y usarlo en Médico
INSERT INTO Medico (nombre, especialidad_id)
SELECT nombre_usuario, 1 FROM Usuario WHERE nombre_usuario = 'medico_auto';


-- Paso 2: Obtener el nombre recién insertado y usarlo en Médico
INSERT INTO Medico (nombre, especialidad_id)
SELECT nombre_usuario, 1 FROM Usuario WHERE nombre_usuario = 'medico1';
