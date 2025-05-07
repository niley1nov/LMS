// src/components/ProfileDropdown.js
import React from "react";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import Divider from "@mui/material/Divider";

/**
 * Props:
 *  - anchorEl: HTML element to anchor the menu
 *  - open: boolean
 *  - onClose: () => void
 *  - onLogout: () => void
 */
export default function ProfileDropdown({ anchorEl, open, onClose, onLogout }) {
  return (
    <Menu
      anchorEl={anchorEl}
      open={open}
      onClose={onClose}
      anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
      transformOrigin={{ vertical: "top", horizontal: "right" }}
      PaperProps={{
        sx: {
          mt: 1,
          bgcolor: "#2a2a2a",
          color: "#fff",
          minWidth: 140,
          borderRadius: 1,
          boxShadow: "0 4px 12px rgba(0,0,0,0.4)",
        },
      }}
    >
      <MenuItem
        onClick={() => {
          onClose();
          alert("Go to Profile");
        }}
        sx={{ color: "#fff" }}
      >
        Profile
      </MenuItem>
      <MenuItem
        onClick={() => {
          onClose();
          alert("Go to Settings");
        }}
        sx={{ color: "#fff" }}
      >
        Settings
      </MenuItem>
      <Divider sx={{ borderColor: "#444" }} />
      <MenuItem
        onClick={() => {
          onLogout();
          onClose();
        }}
        sx={{ color: "#fff" }}
      >
        Logout
      </MenuItem>
    </Menu>
  );
}
