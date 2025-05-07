// src/components/Sidebar.js
import React from "react";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";

const navItems = [
  { label: "Overview", href: "#overview" },
  { label: "Modules", href: "#modules" },
  { label: "Quizzes", href: "#quizzes" },
  { label: "Resources", href: "#resources" },
  { label: "Help & Support", href: "#help" },
];

export default function Sidebar({ isOpen, onClose }) {
  return (
    <Drawer
      anchor="left"
      open={isOpen}
      onClose={onClose}
      ModalProps={{ keepMounted: true }} // improves performance on mobile
      sx={{
        "& .MuiDrawer-paper": {
          width: 240,
          top: "60px", // align below AppBar
          boxSizing: "border-box",
        },
      }}
    >
      <List>
        {navItems.map(({ label, href }) => (
          <React.Fragment key={label}>
            <ListItemButton component="a" href={href} onClick={onClose}>
              <ListItemText primary={label} />
            </ListItemButton>
            <Divider />
          </React.Fragment>
        ))}
      </List>
    </Drawer>
  );
}
