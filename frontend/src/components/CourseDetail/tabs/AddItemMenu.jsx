// src/components/CourseDetail/tabs/AddItemMenu.jsx
import React from "react";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";

function AddItemMenu({ anchorEl, open, onClose, onMenuItemClick }) {
  const options = [
    "Module",
    "Material",
    "Assignment",
    "Video",
    "Quiz",
    "Discussion",
    "External_Link",
  ];

  return (
    <Menu
      anchorEl={anchorEl}
      open={open}
      onClose={onClose}
      anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
      transformOrigin={{ vertical: "top", horizontal: "right" }}
    >
      {options.map((opt) => (
        <MenuItem key={opt} onClick={() => onMenuItemClick(opt)}>
          {opt.replace("_", " ")}
        </MenuItem>
      ))}
    </Menu>
  );
}

export default AddItemMenu;