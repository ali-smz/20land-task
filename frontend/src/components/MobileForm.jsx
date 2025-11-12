import { useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import sampleVideo from "../../assets/sample_video.mp4";
import "react-toastify/dist/ReactToastify.css";

export default function LandingForm() {
  const [mobile, setMobile] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!mobile.trim()) {
      toast.error("شماره موبایل را وارد کنید");
      return;
    }

    try {
      setLoading(true);
      const mobileRegex = /^(?:\+98|0)?9\d{9}$/;

      if (!mobileRegex.test(mobile.trim())) {
        toast.error("شماره موبایل معتبر نیست");
        return;
      }
      const res = await fetch("http://127.0.0.1:8000/api/submit/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ mobile }),
      });

      if (!res.ok) throw new Error("خطا در ارسال داده");

      toast.success("شماره شما با موفقیت ثبت شد");
      setMobile("");
    } catch (err) {
      toast.error("مشکلی در ثبت شماره پیش آمد");
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
            type="text"
            placeholder="مثلاً 09121234567"
            value={mobile}
            onChange={(e) => setMobile(e.target.value)}
            className="w-full p-2 rounded-md outline-none text-right bg-gray-300 text-gray-800 placeholder-gray-500"
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
          <p className="text-gray-300 text-md">
            لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ و با
            استفاده از طراحان گرافیک است چاپگرها و متون بلکه روزنامه و مجله در
            ستون و سطرآنچنان که لازم است و برای شرایط فعلی تکنولوژی مورد نیاز و
            کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد کتابهای زیادی
            در شصت و سه درصد گذشته حال و آینده
          </p>
        </div>
      </form>

      <ToastContainer position="top-center" rtl />
    </div>
  );
}
