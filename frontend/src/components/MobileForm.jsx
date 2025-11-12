import { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import sampleVideo from "../../assets/sample_video.mp4";
import "react-toastify/dist/ReactToastify.css";

const API_BASE = "http://127.0.0.1:8000";

/**
 * Validates Iranian mobile number format
 * Accepts: 09123456789, +989123456789, 989123456789, 9123456789
 */
const validateMobile = (mobile) => {
  const cleaned = mobile.replace(/[\s\-]/g, "");
  // Remove country code prefix if exists
  let normalized = cleaned;
  if (cleaned.startsWith("+98")) {
    normalized = "0" + cleaned.slice(3);
  } else if (cleaned.startsWith("98")) {
    normalized = "0" + cleaned.slice(2);
  } else if (cleaned.startsWith("9") && cleaned.length === 10) {
    normalized = "0" + cleaned;
  }

  // Validate format: should start with 09 and be 11 digits
  const mobileRegex = /^09\d{9}$/;
  return mobileRegex.test(normalized) ? normalized : null;
};

export default function LandingForm() {
  const [mobile, setMobile] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const cleanMobile = mobile.trim();

    if (!cleanMobile) {
      toast.error("شماره موبایل را وارد کنید");
      return;
    }

    // Validate mobile number
    const formatted = validateMobile(cleanMobile);
    if (!formatted) {
      toast.error("شماره موبایل معتبر نیست. فرمت صحیح: 09123456789");
      return;
    }

    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}/api/submit/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobile: formatted }),
      });

      const data = await res.json();

      if (!res.ok) {
        const errorMessage =
          data.error || data.details?.mobile?.[0] || "خطا در ارسال داده";
        throw new Error(errorMessage);
      }

      toast.success("شماره شما با موفقیت ثبت شد");
      setMobile("");
    } catch (err) {
      console.error("Error submitting mobile:", err);
      toast.error(err.message || "مشکلی در ثبت شماره پیش آمد");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden flex items-center justify-center bg-black">
      <video
        className="absolute w-full h-full object-cover opacity-90"
        src={sampleVideo}
        autoPlay
        loop
        muted
      />

      <form
        onSubmit={handleSubmit}
        className="relative z-10 bg-white/20 backdrop-blur-lg px-4 py-10 gap-10 justify-between rounded-2xl shadow-xl flex flex-row-reverse items-center max-sm:mx-5 sm:w-[60%] w-full"
      >
        <div className="lg:w-5/12 w-full">
          <h1 className="text-xl text-right text-white font-semibold mb-4">
            ثبت شماره موبایل
          </h1>

          <input
            type="tel"
            placeholder="مثلاً 09121234567"
            value={mobile}
            onChange={(e) => setMobile(e.target.value)}
            disabled={loading}
            className="w-full p-2 rounded-md outline-none text-right bg-gray-300 text-gray-800 placeholder-gray-500 disabled:opacity-50"
          />

          <button
            type="submit"
            disabled={loading}
            className="mt-4 w-full bg-green-500 hover:bg-green-600 text-white py-2 rounded-md font-semibold transition"
          >
            {loading ? "در حال ثبت ..." : "ثبت"}
          </button>
        </div>

        <div className="lg:w-7/12 hidden lg:block text-right">
          <strong className="text-xl text-white">لورم ایپسوم</strong>
          <p className="text-gray-300 text-md leading-relaxed">
            لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با
            استفاده از طراحان گرافیک است.
          </p>
        </div>
      </form>

      <ToastContainer position="top-center" rtl />
    </div>
  );
}
