"use client";

import React from "react";
import { AlertTriangle } from "lucide-react";

export const SafetyBanner: React.FC = () => {
  return (
    <div className="bg-amber-50/80 border-b border-amber-200/60 px-4 py-2 text-xs text-amber-900 font-sans flex items-center justify-between">
      <div className="max-w-7xl mx-auto flex items-center space-x-2 text-center sm:text-left justify-center sm:justify-start w-full">
        <AlertTriangle className="w-3.5 h-3.5 text-amber-700 shrink-0" />
        <span>
          <strong className="font-semibold">Research and Educational Use Only.</strong> This application does not provide medical diagnoses, treatment recommendations, or clinical interpretations.
        </span>
      </div>
    </div>
  );
};
