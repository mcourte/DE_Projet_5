db = db.getSiblingDB("healthcare_data");

db.createUser({
  user: "evaluateur",
  pwd: "Evaluateur123!",
  roles: [
    { role: "readWrite", db: "healthcare_data" }
  ]
});