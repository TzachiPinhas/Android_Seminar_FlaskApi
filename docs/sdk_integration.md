# SDK Integration Guide

This document explains how to integrate the `booksLib` SDK into your Android application and provides an overview of the example application.

The example application and the SDK library can be found in the following repository: [booksLib Repository on GitHub](https://github.com/TzachiPinhas/booksLib)

## Features

Using the `booksLib` SDK, you can:

- **View the library catalog:** Retrieve all available books.
- **User registration and login:** Easily register and authenticate users.
- **Borrow books:** Submit borrowing requests for available books.
- **Track borrowing history:** View user's borrow records.

---

## Step 1: Adding the Library to Your Project

To use the `booksLib` SDK in your Android project, follow these steps:

1. Add JitPack to your project-level `settings.gradle` file:

   ```gradle
   dependencyResolutionManagement {
       repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
       repositories {
           google()
           mavenCentral()
           maven { url 'https://jitpack.io' }
       }
   }
   ```

2. Add the dependency in your module-level `build.gradle` file:

   ```gradle
   dependencies {
       implementation 'com.github.TzachiPinhas:booksLib:1.0.0'
   }
   ```

---

## Step 2: Examples of using the library in your app

### 1. Initialize the LibraryController

```java
LibraryController libraryController = new LibraryController();
```

### 2. Retrieve All Books

```java
libraryController.getAllBooks(new LibraryController.LibraryCallback<List<Book>>() {
    @Override
    public void onSuccess(List<Book> books) {
        for (Book book : books) {
            Log.d("Book", book.getTitle());
        }
    }

    @Override
    public void onFailure(Throwable t) {
        Log.e("Error", t.getMessage());
    }
});
```

### 3. Register a New User

```java
User newUser = new User("testUser", "password123");
libraryController.register(newUser, new LibraryController.LibraryCallback<LoginResponse>() {
    @Override
    public void onSuccess(LoginResponse response) {
        Log.d("Success", "User registered with ID: " + response.getUserId());
    }

    @Override
    public void onFailure(Throwable t) {
        Log.e("Error", t.getMessage());
    }
});
```

### 4. User Login

```java
User user = new User("testUser", "password123");
libraryController.login(user, new LibraryController.LibraryCallback<String>() {
    @Override
    public void onSuccess(String userId) {
        Log.d("Success", "Logged in user ID: " + userId);
    }

    @Override
    public void onFailure(Throwable t) {
        Log.e("Error", t.getMessage());
    }
});
```

### 5. Borrow a Book

```java
Borrow borrowRequest = new Borrow(userId, bookId);
libraryController.requestBorrow(borrowRequest, new LibraryController.LibraryCallback<Void>() {
    @Override
    public void onSuccess(Void result) {
        Log.d("Success", "Book borrowed successfully");
    }

    @Override
    public void onFailure(Throwable t) {
        Log.e("Error", t.getMessage());
    }
});
```

---

## Step 3: Example Application Overview

The example Android application demonstrates how to use the `booksLib` SDK in practice.

### Features of the Example App:

- **Sign in:** User registration and login.
- **View available books:** Browse the library catalog.
- **Borrow books:** Request books from the catalog.
- **Borrowing history:** Track user's borrowing activity.

## Running the Example Application

The example application and the SDK library can be found in the following repository:

[booksLib Repository on GitHub](https://github.com/TzachiPinhas/booksLib)

### Steps to Run:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TzachiPinhas/booksLib.git
   cd booksLib/exampleapp
   ```

2. **Open the project in Android Studio:**
   - Navigate to `File > Open` and select the `exampleapp` folder.

3. **Build and run the application:**
   - Connect an Android device or start an emulator.
   - Click on `Run` to launch the app and test the integration with the `booksLib` SDK.


## Screenshots
### Sign in
<img src="https://github.com/user-attachments/assets/5eede1a1-5749-4341-a6b2-701bba9afeca" alt="Sign in" width="350" height="700">

### Home - View Available Books & Borrowing
<img src="https://github.com/user-attachments/assets/6a36d27c-63e0-4e80-9873-36ce04d61d52" alt="Home" width="350" height="700">

### Library Catalog
<img src="https://github.com/user-attachments/assets/67a1124e-0a31-43b3-9dd0-975b18245e13" alt="Library Catalog" width="350" height="700">

### Borrowing History
<img src="https://github.com/user-attachments/assets/ffa7c739-2242-4458-b602-9f241c7312db" alt="Borrowing History" width="350" height="700">






