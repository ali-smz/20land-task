// components/MediaDisplay.jsx
import React from "react";

const MediaDisplay = () => {
  return (
    <div className="w-full rounded-lg overflow-hidden shadow-md">
      {/* برای تصویر */}
      <img
        src="https://via.placeholder.com/400x200"
        alt="نمونه"
        className="w-full"
      />

      {/* اگر ویدیو میخوای */}
      {/*
      <video
        src="path_to_video.mp4"
        autoPlay
        loop
        muted
        className="w-full"
      />
      */}
    </div>
  );
};

export default MediaDisplay;
