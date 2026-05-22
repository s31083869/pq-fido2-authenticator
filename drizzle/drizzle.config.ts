import path from "path";
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  dialect: "sqlite",
  dbCredentials: {
    url: path.resolve(__dirname, "../rp_server/data/rp.db")
  },
});