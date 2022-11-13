import { Box } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { DS_DA_BS_data } from "../../data/mockData";
import Header from "../../components/Header";
import { useTheme } from "@mui/material";

const Data_info = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  console.log("data: ", DS_DA_BS_data)

  const columns2 = [
    { field: "id", headerName: "ID", headerAlign: 'center', align:'center' },
    { field: "company_name", headerName: "Company Name", headerAlign: 'center', align:'center' },
    { field: "competitors", headerName: "Competitors", headerAlign: 'center', align:'center' },
    { field: "easy_apply", headerName: "Easy Apply", headerAlign: 'center', align:'center' },
    { field: "founded", headerName: "Founded", headerAlign: 'center', align:'center' },
    { field: "headquarters", headerName: "Headquarters", headerAlign: 'center', align:'center' },
    { field: "industry", headerName: "Industry", headerAlign: 'center', align:'center' },
    { field: "job_description", headerName: "Job Description", headerAlign: 'center', align:'center' },
    { field: "job_title", headerName: "Job Title", headerAlign: 'center', align:'center' },
    { field: "location", headerName: "Location", headerAlign: 'center', align:'center' },
    { field: "rating", headerName: "Rating", headerAlign: 'center', align:'center' },
    { field: "revenue", headerName: "Revenue", headerAlign: 'center', align:'center' },
    { field: "salary_estimate", headerName: "Salary Estimate", headerAlign: 'center', align:'center' },
    { field: "sector", headerName: "Sector", headerAlign: 'center', align:'center' },
    { field: "compnay_size", headerName: "Size", headerAlign: 'center', align:'center' },
    { field: "ownership", headerName: "CompetitoType of ownership", headerAlign: 'center', align:'center' },
    { field: "role", headerName: "role", headerAlign: 'center', align:'center' }
  ]

  const columns = [
    { field: "id", headerName: "ID", flex: 0.5 },
    { field: "registrarId", headerName: "Registrar ID" },
    {
      field: "name",
      headerName: "Name",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "age",
      headerName: "Age",
      type: "number",
      headerAlign: "left",
      align: "left",
    },
    {
      field: "phone",
      headerName: "Phone Number",
      flex: 1,
    },
    {
      field: "email",
      headerName: "Email",
      flex: 1,
    },
    {
      field: "address",
      headerName: "Address",
      flex: 1,
    },
    {
      field: "city",
      headerName: "City",
      flex: 1,
    },
    {
      field: "zipCode",
      headerName: "Zip Code",
      flex: 1,
    },
  ];

  return (
    <Box m="20px">
      <Header
        title="Data Introduction"
        subtitle="The dataset that has been used to this web application."
      />
      <Box
        m="40px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
          "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
            color: `${colors.grey[100]} !important`,
          },
        }}
      >
        <DataGrid
          rows={DS_DA_BS_data}
          columns={columns2}
          components={{ Toolbar: GridToolbar }}
        />
      </Box>
    </Box>
  );
  
};

export default Data_info;
