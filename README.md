# 🤖 Robot-Framework End-to-End Testing Demo

This repository contains a demo project showcasing an example of an end-to-end web testing using [Robot-Framework](https://robotframework.org/), a modern open source Python automation framework. E2E testing allows you to simulate user interactions with your application to ensure its functionality behaves as expected.

## ⚙️ Getting Started

#### 1. Clone the Repository

```bash
git clone https://github.com/KonstantinxVx/e2e-robotframework-demo.git
```
#### 2. Install Requirements:
```bash
cd e2e-robotframework-demo
pip install -r /path/to/requirements.txt
```
#### 3. Run the Tests:
```bash
robot -d results tests
```

## 🧩 Project Structure
The project structure is organized as follows:
- `Libraries/`: contains custom libraries;
- `Resources/`: contains static data and keywords used in tests;
- `Tests/`: contains test files;

## 🧪 Test Cases
The demo project includes E2E tests for the following scenarios:
- Sign up functionality;
- Navigation between pages;
- Form submission and validation;
- Interaction with UI elements;
- Data fetching from API.

## 💼 References:
-  [Robot-framework documentation](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html);
-  [SeleniumLibrary](https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html);
-  [RequestsLibrary](https://docs.robotframework.org/docs/different_libraries/requests);
-  [Selenium](https://www.selenium.dev/).
