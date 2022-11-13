import { Box, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import './team.css';


import jerry_photo from "../../img/jerry.png";
import dong_photo from "../../img/dong.jpeg";
import gene_photo from "../../img/Gene.jpeg";

const Team = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  let message = `There are many variations of passages of Lorem Ipsum available but the \n majority have suffered alteration in some injected humour.`;

  return (
    <Box m="20px">
      <Header title="TEAM" subtitle="Meeting the Team Members" />
      <Box
        m="40px 0 0 0"
        height="75vh"
      >
        <section class="section-white">
          <div class="container">
            <div class="row">
              <div class="col-sm-6 col-md-4">
                <div class="team-item">
                  <img
                    src={jerry_photo}
                    class="team-img"
                    alt="pic"
                  />
                  <h3>Jiale (Jerry) Chen</h3>
                  <div class="team-info">
                    <p>Data Science Fellow, Cohort8</p>
                  </div>
                  <p>
                    City College of New York Applied Mathematics Class of 2023,
                    Interested in Data Science and Finance.
                  </p>

                  <ul class="team-icon">
                    <li>
                      <a href="#" class="twitter">
                        <i class="fa fa-twitter"></i>
                      </a>
                    </li>

                    <li>
                      <a href="#" class="pinterest">
                        <i class="fa fa-pinterest"></i>
                      </a>
                    </li>

                    <li>
                      <a href="#" class="facebook">
                        <i class="fa fa-facebook"></i>
                      </a>
                    </li>

                    <li>
                      <a href="#" class="dribble">
                        <i class="fa fa-dribbble"></i>
                      </a>
                    </li>
                  </ul>
                </div>
              </div>

              <div class="col-sm-6 col-md-4">
                <div class="team-item">
                  <img
                    src={dong_photo}
                    class="team-img"
                    alt="pic"
                  />

                  <h3>Dong Huang Chen</h3>

                  <div class="team-info">
                    <p>Data Science Fellow, Cohort8</p>
                  </div>

                  <p>
                  City College of New York Computer Science Class of 2022.
                  </p>

                  <ul class="team-icon">
                    <li>
                      <a href="#" class="twitter"><i class="fa fa-twitter"></i></a>
                    </li>

                    <li>
                      <a href="#" class="pinterest"><i class="fa fa-pinterest"></i></a>
                    </li>

                    <li>
                      <a href="#" class="facebook"><i class="fa fa-facebook"></i></a>
                    </li>

                    <li>
                      <a href="#" class="dribble"><i class="fa fa-dribbble"></i></a>
                    </li>
                  </ul>
                </div>
              </div>
              <div class="col-sm-6 col-md-4">
                <div class="team-item">
                  <img
                    src={gene_photo}
                    class="team-img"
                    alt="pic"
                  />

                  <h3>Ching Kung Lin</h3>

                  <div class="team-info">
                    <p>Data Science Fellow, Cohort8</p>
                  </div>

                  <p>
                    CUNY Queens College, Computer Science Major, expected to graducate in the end of 2022.
                    Interested in Front-End development, Machine Learning, and Data Science. 
                  </p>

                  <ul class="team-icon">
                    <li>
                      <a href="#" class="twitter"><i class="fa fa-twitter"></i></a>
                    </li>

                    <li>
                      <a href="#" class="pinterest"><i class="fa fa-pinterest"></i></a>
                    </li>

                    <li>
                      <a href="#" class="facebook"><i class="fa fa-facebook"></i></a>
                    </li>

                    <li>
                      <a href="#" class="dribble">
                        <i class="fa fa-dribbble"></i>
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>
      </Box>
      

    </Box>
  );
};

export default Team;
