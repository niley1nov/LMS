// src/components/CourseDetail/tabs/ClassworkTab.jsx
import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import Typography from "@mui/material/Typography";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import AddItemMenu from "./AddItemMenu";
import ArticleIcon from "@mui/icons-material/Article";
import AssignmentIcon from "@mui/icons-material/Assignment";
import OndemandVideoIcon from "@mui/icons-material/OndemandVideo";
import QuizIcon from "@mui/icons-material/Quiz";
import ForumIcon from "@mui/icons-material/Forum";
import LinkIcon from "@mui/icons-material/Link";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";

const getUnitIcon = (type) => {
  switch (type?.toUpperCase()) {
    case "MATERIAL":
      return <ArticleIcon />;
    case "ASSIGNMENT":
      return <AssignmentIcon />;
    case "VIDEO":
      return <OndemandVideoIcon />;
    case "QUIZ":
      return <QuizIcon />;
    case "DISCUSSION":
      return <ForumIcon />;
    case "EXTERNAL_LINK":
      return <LinkIcon />;
    default:
      return <HelpOutlineIcon />;
  }
};

export default function ClassworkTab({ modules, onAddItem }) {
  // state for dropdown menu
  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();
  const { courseId } = useParams();
  const open = Boolean(anchorEl);

  const handleButtonClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleMenuItemClick = (option) => {
    handleClose();
    console.log(`Selected: ${option}`);
    // pick the first module's ID as the default context
     const firstModuleId = modules?.[0]?.id;
     if (!firstModuleId) {
       // no modules yet, maybe prompt user to create one first
       console.warn("No modules available to add a unit to");
       return;
     }

    switch (option) {
      case "Module":
        console.log("Adding a new module");
        navigate(`/courses/${courseId}/modules/new`);
        // Perform module specific action, e.g., open a modal to create a new module
        if (onAddItem) onAddItem("Module");
        break;
      case "Material":
        console.log("Adding new material");
        navigate(`/courses/${courseId}/modules/${firstModuleId}/units/new`);
        // Perform material specific action, e.g., open a modal or navigate to a material creation page
        if (onAddItem) onAddItem("Material");
        break;
      case "Assignment":
        console.log("Adding a new assignment");
        navigate(`/courses/${courseId}/modules/${firstModuleId}/units/new`);
        // Perform assignment specific action, e.g., open an assignment creation form
        if (onAddItem) onAddItem("Assignment");
        break;
      case "Video":
        console.log("Adding a new video");
        navigate(`/courses/${courseId}/modules/${firstModuleId}/units/new`);
        // Perform video specific action, e.g., open a modal to add a video link
        if (onAddItem) onAddItem("Video");
        break;
      case "Quiz":
        console.log("Adding a new quiz");
        navigate(`/courses/${courseId}/modules/${firstModuleId}/units/new`);
        // Perform quiz specific action, e.g., navigate to a quiz builder page
        if (onAddItem) onAddItem("Quiz");
        break;
      case "Discussion":
        console.log("Adding a new discussion forum");
        navigate(`/courses/${courseId}/modules/${firstModuleId}/units/new`);
        // Perform discussion specific action, e.g., open a modal to create a forum topic
        if (onAddItem) onAddItem("Discussion");
        break;
      case "External_Link":
        console.log("Adding an external link");
        navigate(`/courses/${courseId}/modules/${firstModuleId}/units/new`);
        // Perform external link specific action, e.g., open a modal to enter the link URL and title
        if (onAddItem) onAddItem("External_Link");
        break;
      default:
        console.log(`Unknown option selected: ${option}`);
        break;
    }

    // If onAddItem prop is provided, call it with the selected option
    // This allows the parent component to handle the actual item creation logic
    // Otherwise, you might handle navigation directly within this component
    // Example of direct navigation (assuming you have access to a router):
    // if (!onAddItem) {
    //   navigate(`/courses/${id}/new-${option.toLowerCase().replace('_', '-')}`);
    // }
  };

  return (
    <>
      {/* — Add button + dropdown menu — */}
      <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 2 }}>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleButtonClick}
        >
          Add
        </Button>
        {/* Option 2: Using the separate AddItemMenu component */}
        <AddItemMenu
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
          onMenuItemClick={handleMenuItemClick}
        />
      </Box>

      {/* — Existing modules accordion — */}
      {!modules?.length ? (
        <Typography sx={{ fontStyle: "italic", color: "text.disabled", mt: 2 }}>
          No modules have been added to this course yet.
        </Typography>
      ) : (
        modules.map((module, idx) => (
          <Accordion
            key={module.id}
            defaultExpanded={idx === 0}
            sx={{
              mb: 2,
              "&:before": { display: "none" },
              boxShadow: "0px 3px 15px rgba(0,0,0,0.1)",
              borderRadius: "8px",
            }}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls={`module-${module.id}-content`}
              id={`module-${module.id}-header`}
              sx={{
                backgroundColor: "primary.light",
                color: "primary.contrastText",
                borderTopLeftRadius: "8px",
                borderTopRightRadius: "8px",
                "& .MuiAccordionSummary-content": { my: 1.5 },
              }}
            >
              <Typography variant="h6" sx={{ fontWeight: 500 }}>
                {`Module ${module.order ?? idx + 1}: ${module.title}`}
              </Typography>
            </AccordionSummary>

            <AccordionDetails
              sx={{
                p: 0,
                border: "1px solid",
                borderColor: "divider",
                borderTop: "none",
                borderBottomLeftRadius: "8px",
                borderBottomRightRadius: "8px",
              }}
            >
              {module.description && (
                <Typography
                  variant="body2"
                  sx={{
                    p: 2,
                    color: "text.secondary",
                    borderBottom: "1px solid",
                    borderColor: "divider",
                  }}
                >
                  {module.description}
                </Typography>
              )}

              {module.units?.length > 0 ? (
                <List dense disablePadding>
                  {module.units.map((unit, uidx) => (
                    <ListItem
                      key={unit.id}
                      divider={uidx < module.units.length - 1}
                      sx={{
                        py: 1.5,
                        px: 2,
                        "&:hover": { backgroundColor: "action.hover" },
                      }}
                    >
                      <ListItemIcon sx={{ minWidth: 40 }}>
                        {getUnitIcon(unit.type)}
                      </ListItemIcon>
                      <ListItemText
                        primary={`${unit.order ?? uidx + 1}. ${unit.title}`}
                        secondary={
                          unit.type === "EXTERNAL_LINK"
                            ? unit.content
                            : unit.content
                            ? `${unit.content.substring(0, 100)}${
                                unit.content.length > 100 ? "..." : ""
                              }`
                            : null
                        }
                        slotProps={{
                          primary: {
                            sx: { fontWeight: "medium" },
                          },
                        }}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography
                  sx={{ p: 2, fontStyle: "italic", color: "text.disabled" }}
                >
                  No units in this module yet.
                </Typography>
              )}
            </AccordionDetails>
          </Accordion>
        ))
      )}
    </>
  );
}
