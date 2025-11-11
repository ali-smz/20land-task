// components/MobileForm.jsx
import React, { useState } from "react";
import { toast } from "react-toastify";
import MediaDisplay from "./MediaDisplay";
import MobileInput from "./MobileInput";
import SubmitButton from "./UI/SubmitButton";

const MobileForm = () => {
  const [mobile, setMobile] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!mobile.match(/^09\d{9}$/)) {
      toast.error("شماره موبایل معتبر نیست!");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/submit/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ mobile }),
      });

      if (!res.ok) {
        toast.error("خطا در ارسال اطلاعات!");
        setLoading(false);
        return;
      }

      toast.success("شماره با موفقیت ثبت شد!");
      setMobile("");
    } catch (err) {
      toast.error("سرور در دسترس نیست!");
    }

    setLoading(false);
  };

  return (
    <div className="w-full max-w-md">
      <MediaDisplay />
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-lg shadow-md mt-6"
      >
        <MobileInput value={mobile} onChange={setMobile} />
        <SubmitButton loading={loading} />
      </form>
    </div>
  );
};

export default MobileForm;
