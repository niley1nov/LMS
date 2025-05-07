// src/components/CourseCard.js
import React from "react";
import { useNavigate } from "react-router-dom";
import Card from "@mui/material/Card";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import FolderOpenIcon from "@mui/icons-material/FolderOpen";
import ShowChartIcon from "@mui/icons-material/ShowChart";

// Local placeholder image for courses
const DEFAULT_IMAGE = "/default-course.avif";

export default function CourseCard({ course }) {
  const navigate = useNavigate();

  return (
    <Card
      sx={{
        width: 300,
        m: 2,
        display: "flex",
        flexDirection: "column",
        boxShadow: 3,
        borderRadius: 2,
        "&:hover": { boxShadow: 6, cursor: "pointer" },
      }}
      onClick={() => navigate(`/courses/${course.id}`)}
    >
      <CardMedia
        component="img"
        height="140"
        image={course.imageUrl || DEFAULT_IMAGE}
        alt={course.name}
        sx={{ objectFit: "cover" }}
      />

      <CardContent sx={{ flexGrow: 1 }}>
        <Typography
          gutterBottom
          variant="h6"
          component="h3"
          sx={{ fontWeight: "bold" }}
        >
          {course.name}
        </Typography>
        <Typography
          variant="body2"
          color="text.secondary"
          sx={{ lineHeight: 1.5, height: "3em", overflow: "hidden" }}
        >
          {course.description}
        </Typography>
      </CardContent>

      <CardActions sx={{ justifyContent: "flex-end", px: 1, py: 1 }}>
        <IconButton aria-label="statistics" size="small">
          <ShowChartIcon fontSize="small" />
        </IconButton>
        <IconButton aria-label="open folder" size="small">
          <FolderOpenIcon fontSize="small" />
        </IconButton>
        <IconButton aria-label="more options" size="small">
          <MoreVertIcon fontSize="small" />
        </IconButton>
      </CardActions>
    </Card>
  );
}
