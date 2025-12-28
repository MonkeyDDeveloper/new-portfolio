-- ============================================
-- Portfolio Database Schema
-- ============================================
-- FastAPI Portfolio API - MySQL Schema
-- Follows the same structure as the C# .NET project
-- ============================================

-- Drop tables if they exist (in correct order to handle foreign keys)
DROP TABLE IF EXISTS technology_experiences;
DROP TABLE IF EXISTS company_experiences;
DROP TABLE IF EXISTS technology_projects;
DROP TABLE IF EXISTS responsibilities;
DROP TABLE IF EXISTS project_tasks;
DROP TABLE IF EXISTS professional_experiences;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS technologies;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS users;

-- ============================================
-- Authentication Tables
-- ============================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Portfolio Main Entities
-- ============================================

-- Companies table
CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    logo_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Technologies table
CREATE TABLE technologies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    abbr VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_abbr (abbr)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Professional Experiences table
CREATE TABLE professional_experiences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_is_current (is_current),
    INDEX idx_dates (start_date, end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Projects table
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    github_uri VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Related/Child Entities
-- ============================================

-- Project Tasks table (belongs to Project)
CREATE TABLE project_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    project_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_project_id (project_id),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Responsibilities table (belongs to Professional Experience)
CREATE TABLE responsibilities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    experience_id INT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (experience_id) REFERENCES professional_experiences(id) ON DELETE CASCADE,
    INDEX idx_experience_id (experience_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Many-to-Many Relationship Tables
-- ============================================

-- Technology-Project relationship (which technologies were used in which projects)
CREATE TABLE technology_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    technology_id INT NOT NULL,
    project_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE KEY unique_tech_project (technology_id, project_id),
    INDEX idx_technology_id (technology_id),
    INDEX idx_project_id (project_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Company-Experience relationship (which companies are associated with which experiences)
CREATE TABLE company_experiences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    experience_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (experience_id) REFERENCES professional_experiences(id) ON DELETE CASCADE,
    UNIQUE KEY unique_company_experience (company_id, experience_id),
    INDEX idx_company_id (company_id),
    INDEX idx_experience_id (experience_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Technology-Experience relationship (which technologies were used in which experiences)
CREATE TABLE technology_experiences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    technology_id INT NOT NULL,
    experience_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE CASCADE,
    FOREIGN KEY (experience_id) REFERENCES professional_experiences(id) ON DELETE CASCADE,
    UNIQUE KEY unique_tech_experience (technology_id, experience_id),
    INDEX idx_technology_id (technology_id),
    INDEX idx_experience_id (experience_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Real Portfolio Data
-- ============================================

-- Insert admin user (password is hashed 'Juan123!' using bcrypt)
INSERT INTO users (username, email, password) VALUES
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYq3HCqnqeS');

-- Insert companies
INSERT INTO companies (id, name, logo_path) VALUES
(1, 'MonkeyDDeveloper', '/experience/monkey_d_developer.png'),
(2, 'Soluciones y Proyectos SA', '/experience/nomina360.png'),
(3, 'Cacao Web Studio', '/experience/cacao_logo.jpg'),
(4, 'Dacodes', '/experience/dacodes_logo.webp');

-- Insert professional experiences
INSERT INTO professional_experiences (id, title, description, start_date, end_date, is_current) VALUES
(1, 'FullStack Developer at MonkeyDDevelopment', 'We created a web application to streamline the student enrollment process.', '2021-02-01', '2022-07-31', FALSE),
(2, 'FullStack Developer at Soluciones y Proyectos SA', 'Implemented Nomina360, a web app for human resources management.', '2022-10-01', '2023-11-30', FALSE),
(3, 'Frontend Developer at CacaoWebStudio', 'Developed a client''s page using the new version of Shopify Theme Dawn.', '2023-11-01', '2024-02-29', FALSE),
(4, 'Software Engineer at Dacodes', 'Created an application to manage the capacitation of operators in Yucatán, México.', '2024-05-01', '2024-12-31', TRUE);

-- Insert responsibilities
INSERT INTO responsibilities (id, experience_id, description) VALUES
-- FullStack Developer at MonkeyDDevelopment
(1, 1, 'Defining the current enrollment process and its weaknesses.'),
(2, 1, 'Design the pages and use cases, with focus on easy use for its users.'),
(3, 1, 'Make reviews with the administrative staff and the students of the institute.'),
(4, 1, 'Define the correct structure of subjects, students, careers, admin users for the database.'),
(5, 1, 'Be responsible for the frontend, backend, database and release of the application.'),

-- FullStack Developer at Soluciones y Proyectos SA
(6, 2, 'Implement readable and clean code, following the best practices.'),
(7, 2, 'Analyze the requirements to implement them correctly.'),
(8, 2, 'Realize unit testing of the functions created.'),
(9, 2, 'Have great communication with the rest of the dev team, and also with the administrative team.'),
(10, 2, 'Realize code review of the tasks of the rest of the team.'),

-- Frontend Developer at CacaoWebStudio
(11, 3, 'Efficiently implement components, snippets, and sections of Shopify.'),
(12, 3, 'Testing every new section created to ensure its working in different screen sizes.'),
(13, 3, 'Priority user experience, make efficient js code.'),
(14, 3, 'Defining project structure.'),
(15, 3, 'Keep track of tasks and good communication with the designing and development team.'),
(16, 3, 'Ensure clean and understandable code (code review).'),

-- Software Engineer at Dacodes
(17, 4, 'Create and implement Vuejs components using domain-driven-design.'),
(18, 4, 'Estimate the time to implement requirements in hours in meetings with the team.'),
(19, 4, 'Follow the business requirements and use cases.'),
(20, 4, 'Good communication with the QA and development team.'),
(21, 4, 'Ensure clean and understandable code and code refactorization.'),
(22, 4, 'Side help with Backend code analysis and DB.');

-- Insert technologies (54 technologies)
INSERT INTO technologies (id, name, abbr) VALUES
(1, 'Nuxt 3.10.2', 'nuxt'),
(2, 'Vue.js 3.4.x', 'vue'),
(3, 'Vue.js 2.7', 'vue'),
(4, 'Vuetify 2.6', 'vuetify'),
(5, 'Bootstrap 4.x', 'bootstrap'),
(6, 'Nuxt/ui 2.13.0', 'nuxtui'),
(7, 'TailwindCSS 3.4.1', 'tailwind'),
(8, 'Zod 3.2.24', 'zod'),
(9, 'Node 20.0.0', 'node'),
(10, 'PostgreSQL 12', 'postgres'),
(11, 'Git', 'git'),
(12, 'Docker', 'docker'),
(13, 'Nuxt 3.10.2', 'nuxt'),
(14, 'Vue.js 3.4.x', 'vue'),
(15, 'Nuxt/ui 2.13.0', 'nuxtui'),
(16, 'TailwindCSS 3.4.1', 'tailwind'),
(17, 'Zod 3.2.24', 'zod'),
(18, 'Node 20.0.0', 'node'),
(19, 'i18n 8.1.1', 'i18n'),
(20, 'Resend 3.2.0', 'resend'),
(21, 'Shopify Dawn 13.0.1', 'shopify'),
(22, 'Liquid Template Language 5.4.0', 'liquidtemplate'),
(23, 'Git', 'git'),
(24, 'Vue.js 3.2.3', 'vue'),
(25, 'Node 10.24.0', 'node'),
(26, 'Quasar Framework 0.17', 'quasar'),
(27, 'MongoDB 5.0', 'mongo'),
(28, 'TypeScript 5.4', 'typescript'),
(29, 'JavaScript (Vanilla)', 'javascript'),
(30, 'Pug.js (HTML)', 'pugjs'),
(31, 'Bootstrap 5.0', 'bootstrap'),
(32, 'Node.js 14.0.0', 'node'),
(33, 'Express 4.0', 'express'),
(34, 'MongoDB 5.0', 'mongo'),
(35, 'DigitalOcean', 'digitalocean'),
(36, 'Nginx', 'nginx'),
(37, 'NameCheap', 'namecheap'),
(38, 'JsonWebTokens', 'jwt'),
(39, 'Python 3.10.12', 'python'),
(40, 'Flask 3.0.3', 'flask'),
(41, 'PyMongo 4.7.2', 'pymongo'),
(42, 'Mongoose', 'mongoose'),
(43, 'AWS API Gateway', 'awsgateway'),
(44, 'AWS Lambda Functions', 'awslambda'),
(45, 'Nextjs', 'nextjs'),
(46, 'PostgreSQL', 'postgres'),
(47, '.NET 8', 'DotNET'),
(48, 'Entity Framework', 'entityframework'),
(49, 'Digital Ocean Droplets', 'digitalocean'),
(50, 'Github Actions', 'githubactions'),
(51, 'Redis', 'redis'),
(52, 'Swagger', 'swagger'),
(53, 'Jest', 'jest'),
(54, 'Axios', 'axios');

-- Insert technology-experience relationships
INSERT INTO technology_experiences (id, technology_id, experience_id) VALUES
-- Dacodes (Experience 4)
(1, 1, 4), (2, 2, 4), (3, 3, 4), (4, 4, 4), (5, 5, 4), (6, 6, 4),
(7, 7, 4), (8, 8, 4), (9, 9, 4), (10, 10, 4), (11, 11, 4), (12, 12, 4),
-- CacaoWebStudio (Experience 3)
(13, 13, 3), (14, 14, 3), (15, 16, 3), (16, 17, 3), (17, 18, 3),
(18, 19, 3), (19, 20, 3), (20, 21, 3), (21, 22, 3),
-- Soluciones y Proyectos SA (Experience 2)
(22, 24, 2), (23, 25, 2), (24, 26, 2), (25, 27, 2), (26, 28, 2),
(36, 53, 2), (37, 52, 2),
-- MonkeyDevelopment (Experience 1)
(27, 29, 1), (28, 30, 1), (29, 31, 1), (30, 32, 1), (31, 33, 1),
(32, 34, 1), (33, 35, 1), (34, 36, 1), (35, 37, 1);

-- Insert company-experience relationships
INSERT INTO company_experiences (id, company_id, experience_id) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4);

-- Insert projects
INSERT INTO projects (id, name, description, github_uri) VALUES
(1, 'Dockerized Product Management System with Authentication', 'Full stack application that uses JWT to auth. The front was built with Nuxtjs and the back with express, both of them usgin typescript. It is dockerized and uses a Mongo Database. ', 'https://github.com/MonkeyDDeveloper/dockerized-full-stack-application'),
(2, 'Dockerized Python Flask Rest Api - MongoDB', 'An example of rest api using Flask library and an ORM to connect and interact with a Mongo Database.', 'https://github.com/MonkeyDDeveloper/dockerized-flask-api-mongodb'),
(3, 'Api Gateway - Lambda Functions Rest Api', 'AWS Lambda funtions as microservices built with TypeScript to create a rest api.', 'https://github.com/MonkeyDDeveloper/aws-lambda-apigateway-functions'),
(4, 'Dockerized Portfolio - .Net - Postgres', 'The page you are watching, it was built using nextjs, typescript, .net and postgres as database. Also, it is deployed automatically using github actions in a digital ocean droplet.', 'https://github.com/MonkeyDDeveloper/workflows'),
(5, 'TypeScript Api', 'Dockerized TypeScript Api that uses Redis db to caching data. It implements Swagger Docs, and Jest for testing.', 'https://github.com/MonkeyDDeveloper/api-ts-swagger'),
(6, 'Python CLI CRUD with Postgres', 'CRUD with Python using Psycopg2, Docker, Postgres SQL Scripts, Bcrypt, PrettyTable and email-validator', 'https://github.com/MonkeyDDeveloper/python_console_crud');

-- Insert technology-project relationships
INSERT INTO technology_projects (id, project_id, technology_id) VALUES
-- Project 1: Dockerized Product Management System
(1, 1, 1), (2, 1, 2), (3, 1, 6), (4, 1, 11), (5, 1, 12),
(6, 1, 33), (7, 1, 34), (8, 1, 28), (9, 1, 38),
-- Project 2: Flask API
(10, 2, 12), (11, 2, 39), (12, 2, 40), (13, 2, 41),
-- Project 3: AWS Lambda
(14, 3, 42), (15, 3, 43), (16, 3, 44), (17, 3, 28),
-- Project 4: Portfolio .NET
(18, 4, 45), (19, 4, 46), (20, 4, 47), (21, 4, 48),
(22, 4, 49), (23, 4, 50), (24, 4, 28), (25, 4, 12), (26, 4, 23),
-- Project 5: TypeScript API
(27, 5, 51), (28, 5, 52), (29, 5, 53), (30, 5, 54),
(31, 5, 49), (32, 5, 23), (33, 5, 12), (34, 5, 9),
-- Project 6: Python CLI
(35, 6, 46), (36, 6, 39), (37, 6, 23), (38, 6, 12);

-- ============================================
-- End of Schema
-- ============================================
