import argparse

from pyspark.sql import SparkSession


def calculate_red_violations(data_source, output_uri):
    with SparkSession.builder.appName("Calculate Red Health Violations").getOrCreate() as spark:
        # Load the restaurant violation CSV data
        if data_source is not None:
            restaurants_df = spark.read.option(
                "header", "true").csv(data_source)

        # Create an in-memory DataFrame to query
        restaurants_df.createOrReplaceTempView("restaurant_violations")

        # Create a DataFrame of the top 10 restaurants with the most Red violations
        top_red_violation_restaurants = spark.sql("SELECT name, count(*) AS total_red_violations " +
                                                  "FROM restaurant_violations " +
                                                  "WHERE violation_type = 'RED' " +
                                                  "GROUP BY name " +
                                                  "ORDER BY total_red_violations DESC LIMIT 10 ")

        # Write the results to the specified output URI
        top_red_violation_restaurants.write.option(
            "header", "true").mode("overwrite").csv(output_uri)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_source')
    parser.add_argument('--output_uri')
    args = parser.parse_args()

    calculate_red_violations(args.data_source, args.output_uri)
