-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 16-05-2024 a las 01:04:24
-- Versión del servidor: 8.0.17
-- Versión de PHP: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `presupuesto`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `ID_cliente` int(11) NOT NULL,
  `CUIT` varchar(255) DEFAULT NULL,
  `Razon_social` varchar(255) DEFAULT NULL,
  `Direccion` varchar(255) DEFAULT NULL,
  `Ubicacion_geografica` varchar(255) DEFAULT NULL,
  `N_contacto` varchar(255) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `apellido` varchar(255) DEFAULT NULL,
  `Unidad_de_negocio` varchar(255) DEFAULT NULL,
  `Legajo_vendedor` int(11) DEFAULT NULL,
  `Facturacion_anual` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`ID_cliente`, `CUIT`, `Razon_social`, `Direccion`, `Ubicacion_geografica`, `N_contacto`, `nombre`, `apellido`, `Unidad_de_negocio`, `Legajo_vendedor`, `Facturacion_anual`) VALUES
(1, '20-36528392-4', 'a', 's', 'd', '1', 'a', 's', 'd', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `items`
--

CREATE TABLE `items` (
  `ID_items` int(11) NOT NULL,
  `ID_presupuesto` int(11) DEFAULT NULL,
  `Cantidad` int(11) DEFAULT NULL,
  `precio_por_unidad` float DEFAULT NULL,
  `importe` float GENERATED ALWAYS AS ((`Cantidad` * `precio_por_unidad`)) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `presupuestos`
--

CREATE TABLE `presupuestos` (
  `ID_presupuesto` int(11) NOT NULL,
  `Legajo_vendedor` int(11) NOT NULL,
  `ID_cliente` int(11) NOT NULL,
  `Entrega_incluido` varchar(255) DEFAULT NULL,
  `Fecha_envio` varchar(255) DEFAULT NULL,
  `comentario` text,
  `Condiciones` text,
  `subtotal` float DEFAULT NULL,
  `IVA_21` float GENERATED ALWAYS AS ((`subtotal` * 0.21)) STORED,
  `total` float GENERATED ALWAYS AS ((`subtotal` * 1.21)) STORED,
  `fecha_presupuesto` datetime DEFAULT CURRENT_TIMESTAMP,
  `tiempo_dias_valido` int(11) DEFAULT NULL,
  `fecha_caducidad` datetime GENERATED ALWAYS AS ((`fecha_presupuesto` + interval `tiempo_dias_valido` day)) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vendedores`
--

CREATE TABLE `vendedores` (
  `ID_vendedor` int(11) NOT NULL,
  `Legajo_vendedor` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`ID_cliente`);

--
-- Indices de la tabla `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`ID_items`),
  ADD KEY `ID_presupuesto` (`ID_presupuesto`);

--
-- Indices de la tabla `presupuestos`
--
ALTER TABLE `presupuestos`
  ADD PRIMARY KEY (`ID_presupuesto`);

--
-- Indices de la tabla `vendedores`
--
ALTER TABLE `vendedores`
  ADD PRIMARY KEY (`Legajo_vendedor`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `ID_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `items`
--
ALTER TABLE `items`
  MODIFY `ID_items` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `presupuestos`
--
ALTER TABLE `presupuestos`
  MODIFY `ID_presupuesto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `vendedores`
--
ALTER TABLE `vendedores`
  MODIFY `Legajo_vendedor` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `items`
--
ALTER TABLE `items`
  ADD CONSTRAINT `items_ibfk_1` FOREIGN KEY (`ID_presupuesto`) REFERENCES `presupuestos` (`ID_presupuesto`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
