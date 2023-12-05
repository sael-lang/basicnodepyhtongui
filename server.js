// Install the necessary packages using npm:
// npm install express mongoose body-parser
//node filename.js
const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");

const app = express();
const port = 3000;

// Connect to MongoDB
mongoose.connect("mongodb://localhost:27017/schoolDB", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});
const db = mongoose.connection;

// Define the mongoose schema for School, Address, and Organization
const addressSchema = new mongoose.Schema({
  city: String,
  state: String,
  country: String,
});

const organizationSchema = new mongoose.Schema({
  name: String,
  type: String,
});

const schoolSchema = new mongoose.Schema({
  name: String,
  address: addressSchema,
  organization: organizationSchema,
});

const Address = mongoose.model("Address", addressSchema);
const Organization = mongoose.model("Organization", organizationSchema);
const School = mongoose.model("School", schoolSchema);

app.use(bodyParser.json());

// POST endpoint to save JSON document into MongoDB
app.post("/api/schools", async (req, res) => {
  try {
    const { name, address, organization } = req.body;

    // Save Address
    const savedAddress = await Address.create(address);

    // Save Organization
    const savedOrganization = await Organization.create(organization);

    // Save School with references to Address and Organization
    const school = new School({
      name,
      address: savedAddress,
      organization: savedOrganization,
    });

    const savedSchool = await school.save();

    res.status(201).json(savedSchool);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// PUT endpoint to update existing document or create a new one
app.put("/api/schools", async (req, res) => {
  try {
    const { name, address, ...updatedFields } = req.body;

    // Find School by name and address
    const existingSchool = await School.findOne({
      name,
      "address.city": address.city,
      "address.state": address.state,
    });

    if (existingSchool) {
      // Update existing School
      existingSchool.set(updatedFields);
      const updatedSchool = await existingSchool.save();
      res.json(updatedSchool);
    } else {
      // Create new School
      const savedAddress = await Address.create(address);
      const school = new School({
        name,
        address: savedAddress,
        ...updatedFields,
      });
      const savedSchool = await school.save();
      res.status(201).json(savedSchool);
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// GET endpoint to get a document by ID
app.get("/api/schools/:id", async (req, res) => {
  try {
    const school = await School.findById(req.params.id);
    res.json(school);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// GET endpoint to get a list of all schools
app.get("/api/schools", async (req, res) => {
  try {
    const schools = await School.find();
    res.json(schools);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// DELETE endpoint to delete a document by ID
app.delete("/api/schools/:id", async (req, res) => {
  try {
    await School.findByIdAndDelete(req.params.id);
    res.sendStatus(204);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
