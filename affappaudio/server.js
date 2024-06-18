require("dotenv").config();
const mongoose = require("mongoose");
const express = require("express");
const session = require("express-session");
const MongoStore = require('connect-mongo');
const bodyParser = require('body-parser');
const authRoutes = require("./routes/authRoutes");
const webhookRoutes = require("./routes/webhookRoutes");

console.log("Starting server...");

if (!process.env.DATABASE_URL || !process.env.SESSION_SECRET) {
  console.error("Error: config environment variables not set. Please create/edit .env configuration file.");
  process.exit(-1);
}

const app = express();
const port = process.env.PORT || 3000;

try {
  // Middleware to parse request bodies
  app.use(bodyParser.json());
  app.use(bodyParser.urlencoded({ extended: true }));

  console.log("Middleware setup complete.");

  // Setting the templating engine to EJS
  app.set("view engine", "ejs");

  // Serve static files
  app.use(express.static("public"));

  console.log("Static files middleware setup complete.");

  // Database connection
  mongoose
    .connect(process.env.DATABASE_URL)
    .then(() => {
      console.log("Database connected successfully");
    })
    .catch((err) => {
      console.error(`Database connection error: ${err.message}`);
      console.error(err.stack);
      process.exit(1);
    });

  // Session configuration with connect-mongo
  app.use(
    session({
      secret: process.env.SESSION_SECRET,
      resave: false,
      saveUninitialized: false,
      store: MongoStore.create({ mongoUrl: process.env.DATABASE_URL }),
    }),
  );

  app.on("error", (error) => {
    console.error(`Server error: ${error.message}`);
    console.error(error.stack);
  });

  process.on('uncaughtException', (error) => {
    console.error(`Uncaught Exception: ${error.message}`);
    console.error(error.stack);
  });

  process.on('unhandledRejection', (reason, promise) => {
    console.error(`Unhandled Rejection at: ${promise}, reason: ${reason}`);
  });

  // Logging session creation and destruction
  app.use((req, res, next) => {
    const sess = req.session;
    // Make session available to all views
    res.locals.session = sess;
    if (!sess.views) {
      sess.views = 1;
      console.log("Session created at: ", new Date().toISOString());
    } else {
      sess.views++;
      console.log(
        `Session accessed again at: ${new Date().toISOString()}, Views: ${sess.views}, User ID: ${sess.userId || '(unauthenticated)'}`,
      );
    }
    next();
  });

  // Authentication Routes
  app.use(authRoutes);
  console.log("Auth routes registered.");

  // Webhook Routes
  app.use(webhookRoutes);
  console.log("Webhook routes registered.");

  // Root path response
  app.get("/", (req, res) => {
    res.render("index");
    console.log("Root path accessed.");
  });

  // If no routes handled the request, it's a 404
  app.use((req, res, next) => {
    res.status(404).send("Page not found.");
    console.log("404 - Page not found.");
  });

  // Error handling
  app.use((err, req, res, next) => {
    console.error(`Unhandled application error: ${err.message}`);
    console.error(err.stack);
    res.status(500).send("There was an error serving your request.");
  });

  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });
} catch (error) {
  console.error(`Server setup failed: ${error.message}`);
  console.error(error.stack);
  process.exit(1);
}