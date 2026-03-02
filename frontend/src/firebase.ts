import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDOMkovBJN05w13Rmja81Mlgea7P2cREIQ",
  authDomain: "edziennik-modea.firebaseapp.com",
  projectId: "edziennik-modea",
  storageBucket: "edziennik-modea.firebasestorage.app",
  messagingSenderId: "2073425274",
  appId: "1:2073425274:web:94b80fbdad60eeeaeed2c3",
  measurementId: "G-DLCC8P8JS5"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export default app;
